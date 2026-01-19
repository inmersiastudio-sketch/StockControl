"""
Modelos de Venta y Items de Venta
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Sale(Base):
    """
    Registro de venta.
    Cada venta tiene múltiples items (productos vendidos).
    """
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Totales
    subtotal = Column(Float, nullable=False)
    discount = Column(Float, default=0)  # Descuento aplicado
    total = Column(Float, nullable=False)
    
    # Pago
    payment_method = Column(String(20), nullable=False)  # 'cash', 'card', 'transfer'
    amount_paid = Column(Float, nullable=True)  # Para calcular vuelto en efectivo
    change_given = Column(Float, nullable=True)  # Vuelto entregado
    
    # Usuario que realizó la venta
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Cancelación
    is_cancelled = Column(Boolean, default=False)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    cancel_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    user = relationship("User", foreign_keys=[user_id])
    cancelled_by = relationship("User", foreign_keys=[cancelled_by_id])
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    
    @property
    def profit(self) -> float:
        """Calcular ganancia total de la venta"""
        return sum(item.profit for item in self.items)
    
    def __repr__(self):
        return f"<Sale {self.id}: ${self.total}>"


class SaleItem(Base):
    """
    Item individual de una venta.
    Guarda el costo al momento de la venta para calcular ganancia.
    """
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # Precio de venta al momento
    unit_cost = Column(Float, nullable=False)  # Costo al momento (para calcular ganancia)
    subtotal = Column(Float, nullable=False)  # quantity * unit_price
    
    # Relaciones
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")
    
    @property
    def profit(self) -> float:
        """Ganancia de este item"""
        return (self.unit_price - self.unit_cost) * self.quantity
    
    def __repr__(self):
        return f"<SaleItem {self.quantity}x {self.product_id}>"
