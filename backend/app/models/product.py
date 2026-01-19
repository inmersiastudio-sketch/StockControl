"""
Modelos de Producto y Lotes (para FIFO)
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Product(Base):
    """
    Producto del catálogo.
    El costo es el costo promedio calculado de los lotes.
    """
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # Código interno o de barras
    barcode = Column(String(50), nullable=True, index=True)  # Código de barras EAN
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Precio y costo
    cost = Column(Float, default=0)  # Costo promedio calculado
    price = Column(Float, nullable=False)  # Precio de venta
    
    # Stock
    min_stock = Column(Integer, default=10)  # Alerta de stock bajo
    
    # Estado
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    category = relationship("Category", back_populates="products")
    lots = relationship("ProductLot", back_populates="product", order_by="ProductLot.expiration_date")
    sale_items = relationship("SaleItem", back_populates="product")
    purchase_items = relationship("PurchaseItem", back_populates="product")
    
    @property
    def current_stock(self) -> int:
        """Calcular stock total sumando todos los lotes activos"""
        return sum(lot.quantity for lot in self.lots if lot.quantity > 0)
    
    @property
    def margin_percentage(self) -> float:
        """Calcular margen de ganancia en porcentaje"""
        if self.price <= 0:
            return 0
        return ((self.price - self.cost) / self.price) * 100
    
    def __repr__(self):
        return f"<Product {self.code}: {self.name}>"


class ProductLot(Base):
    """
    Lote de producto para manejo FIFO.
    Cada compra crea un nuevo lote con su fecha de vencimiento.
    Las ventas descuentan del lote más antiguo/próximo a vencer.
    """
    __tablename__ = "product_lots"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)  # Cantidad actual en este lote
    initial_quantity = Column(Integer, nullable=False)  # Cantidad inicial
    cost = Column(Float, nullable=False)  # Costo unitario de este lote
    
    expiration_date = Column(Date, nullable=True)  # Fecha de vencimiento
    
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    product = relationship("Product", back_populates="lots")
    purchase = relationship("Purchase", back_populates="lots")
    
    @property
    def is_expired(self) -> bool:
        """Verificar si el lote está vencido"""
        if not self.expiration_date:
            return False
        from datetime import date
        return self.expiration_date < date.today()
    
    def __repr__(self):
        return f"<ProductLot {self.id}: {self.quantity} units, exp: {self.expiration_date}>"
