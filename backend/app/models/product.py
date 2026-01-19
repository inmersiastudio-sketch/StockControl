"""
Modelo de Producto
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    cost = Column(Float, default=0.0, nullable=False)  # Costo promedio
    price = Column(Float, nullable=False)  # Precio de venta
    min_stock = Column(Integer, default=10, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    category = relationship("Category", back_populates="products")
    lots = relationship("ProductLot", back_populates="product", cascade="all, delete-orphan")
    purchase_items = relationship("PurchaseItem", back_populates="product")
    sale_items = relationship("SaleItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, code='{self.code}', name='{self.name}')>"

    @property
    def current_stock(self):
        """Stock total actual (suma de todos los lotes)"""
        return sum(lot.quantity for lot in self.lots if lot.quantity > 0)

    @property
    def margin_percentage(self):
        """Margen de ganancia en porcentaje"""
        if self.price == 0:
            return 0
        return ((self.price - self.cost) / self.price) * 100

    @property
    def next_expiration_date(self):
        """Próxima fecha de vencimiento"""
        active_lots = [lot for lot in self.lots if lot.quantity > 0 and lot.expiration_date]
        if not active_lots:
            return None
        return min(lot.expiration_date for lot in active_lots)
