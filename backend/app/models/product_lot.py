"""
Modelo de Lote de Producto (para FIFO)
"""

from datetime import date as date_type
from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProductLot(Base):
    __tablename__ = "product_lots"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=True)
    quantity = Column(Integer, nullable=False)  # Cantidad restante en lote
    initial_quantity = Column(Integer, nullable=False, default=0)  # Cantidad inicial del lote
    cost = Column(Float, nullable=False)  # Costo unitario de este lote
    expiration_date = Column(Date, nullable=True, index=True)  # Fecha de vencimiento
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    product = relationship("Product", back_populates="lots")
    purchase = relationship("Purchase", back_populates="lots")
    
    @property
    def is_expired(self):
        """Verificar si el lote está vencido"""
        if self.expiration_date:
            return self.expiration_date < date_type.today()
        return False

    def __repr__(self):
        return f"<ProductLot(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, exp={self.expiration_date})>"
