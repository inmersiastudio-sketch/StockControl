"""
Modelo de Venta
"""

from sqlalchemy import Column, Integer, Float, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    subtotal = Column(Float, nullable=False, default=0.0)  # Total antes de descuento
    total = Column(Float, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    payment_method = Column(String(20), nullable=False)  # 'cash', 'card', 'transfer'
    amount_paid = Column(Float, nullable=True)  # Monto pagado por el cliente
    change_given = Column(Float, default=0.0, nullable=True)  # Vuelto entregado
    
    # Campos para devoluciones
    is_cancelled = Column(Boolean, default=False, nullable=False, index=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    cancel_reason = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relaciones
    user = relationship("User", back_populates="sales", foreign_keys=[user_id])
    cancelled_by_user = relationship("User", back_populates="cancelled_sales", foreign_keys=[cancelled_by])
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")

    @property
    def total_profit(self):
        """Ganancia total de la venta"""
        return sum(item.profit for item in self.items)
    
    @property
    def user_name(self):
        """Nombre del usuario que realizó la venta"""
        return self.user.full_name if self.user else ""

    def __repr__(self):
        return f"<Sale(id={self.id}, user_id={self.user_id}, total={self.total}, cancelled={self.is_cancelled})>"
