"""
Modelo de Item de Compra (detalle)
"""

from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)  # Costo unitario
    expiration_date = Column(Date, nullable=True)

    # Relaciones
    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product", back_populates="purchase_items")

    @property
    def subtotal(self):
        return self.quantity * self.cost

    def __repr__(self):
        return f"<PurchaseItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
