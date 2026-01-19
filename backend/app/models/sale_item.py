"""
Modelo de Item de Venta (detalle)
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # Precio al momento de la venta
    unit_cost = Column(Float, nullable=False)  # Costo real (de FIFO)
    subtotal = Column(Float, nullable=False)  # quantity * unit_price

    # Relaciones
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")

    @property
    def profit(self):
        """Ganancia de este item"""
        return (self.unit_price - self.unit_cost) * self.quantity

    def __repr__(self):
        return f"<SaleItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
