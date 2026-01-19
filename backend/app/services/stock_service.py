"""
Servicio de gestión de Stock con lógica FIFO
TODO: Implementar en Sprint 3
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.models.product import Product, ProductLot


class StockService:
    """
    Servicio para manejar el stock de productos usando FIFO
    (First In, First Out basado en fecha de vencimiento)
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_available_stock(self, product_id: int) -> int:
        """
        Obtener stock total disponible de un producto
        (suma de todos los lotes con cantidad > 0)
        """
        lots = self.db.query(ProductLot).filter(
            ProductLot.product_id == product_id,
            ProductLot.quantity > 0
        ).all()
        
        return sum(lot.quantity for lot in lots)
    
    def add_stock(
        self,
        product_id: int,
        quantity: int,
        cost: float,
        expiration_date: Optional[date] = None,
        purchase_id: Optional[int] = None
    ) -> ProductLot:
        """
        Agregar stock creando un nuevo lote
        """
        lot = ProductLot(
            product_id=product_id,
            quantity=quantity,
            initial_quantity=quantity,
            cost=cost,
            expiration_date=expiration_date,
            purchase_id=purchase_id
        )
        
        self.db.add(lot)
        self.db.commit()
        self.db.refresh(lot)
        
        # Actualizar costo promedio del producto
        self._update_average_cost(product_id)
        
        return lot
    
    def remove_stock(self, product_id: int, quantity: int) -> List[dict]:
        """
        Remover stock usando FIFO (primero que vence, primero sale)
        
        Returns:
            Lista de diccionarios con info de cada lote usado:
            [{"lot_id": 1, "quantity": 5, "cost": 100.0}, ...]
        """
        # Obtener lotes ordenados por fecha de vencimiento (FIFO)
        lots = self.db.query(ProductLot).filter(
            ProductLot.product_id == product_id,
            ProductLot.quantity > 0
        ).order_by(
            ProductLot.expiration_date.asc().nullslast(),
            ProductLot.created_at.asc()
        ).all()
        
        remaining = quantity
        used_lots = []
        
        for lot in lots:
            if remaining <= 0:
                break
            
            take = min(lot.quantity, remaining)
            lot.quantity -= take
            remaining -= take
            
            used_lots.append({
                "lot_id": lot.id,
                "quantity": take,
                "cost": lot.cost
            })
        
        if remaining > 0:
            raise ValueError(f"Stock insuficiente. Faltan {remaining} unidades.")
        
        self.db.commit()
        return used_lots
    
    def restore_stock(self, product_id: int, quantity: int, lot_info: List[dict]):
        """
        Restaurar stock (para devoluciones)
        Intenta devolver al lote original si aún existe
        """
        for info in lot_info:
            lot = self.db.query(ProductLot).filter(
                ProductLot.id == info["lot_id"]
            ).first()
            
            if lot:
                lot.quantity += info["quantity"]
            else:
                # Si el lote ya no existe, crear uno nuevo
                self.add_stock(
                    product_id=product_id,
                    quantity=info["quantity"],
                    cost=info["cost"]
                )
        
        self.db.commit()
    
    def get_weighted_average_cost(self, product_id: int) -> float:
        """
        Calcular costo promedio ponderado del stock actual
        """
        lots = self.db.query(ProductLot).filter(
            ProductLot.product_id == product_id,
            ProductLot.quantity > 0
        ).all()
        
        total_quantity = sum(lot.quantity for lot in lots)
        if total_quantity == 0:
            return 0
        
        total_cost = sum(lot.quantity * lot.cost for lot in lots)
        return total_cost / total_quantity
    
    def _update_average_cost(self, product_id: int):
        """
        Actualizar el costo promedio en el producto
        """
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.cost = self.get_weighted_average_cost(product_id)
            self.db.commit()
    
    def get_expiring_soon(self, days: int = 7) -> List[ProductLot]:
        """
        Obtener lotes que vencen pronto
        """
        from datetime import timedelta
        
        limit_date = date.today() + timedelta(days=days)
        
        return self.db.query(ProductLot).filter(
            ProductLot.quantity > 0,
            ProductLot.expiration_date != None,
            ProductLot.expiration_date <= limit_date
        ).order_by(ProductLot.expiration_date).all()
    
    def get_low_stock_products(self) -> List[Product]:
        """
        Obtener productos con stock bajo (menor al mínimo)
        """
        products = self.db.query(Product).filter(Product.is_active == True).all()
        
        low_stock = []
        for product in products:
            current_stock = self.get_available_stock(product.id)
            if current_stock < product.min_stock:
                low_stock.append(product)
        
        return low_stock
