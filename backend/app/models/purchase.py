"""
Modelo de Compra a Proveedor
"""

from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    
    # ⭐ Campos para OCR
    receipt_image_path = Column(String(255), nullable=True)  # Ruta a imagen del ticket
    ocr_data = Column(JSON, nullable=True)  # Datos extraídos por OCR (JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relaciones
    supplier = relationship("Supplier", back_populates="purchases")
    user = relationship("User", back_populates="purchases")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")
    lots = relationship("ProductLot", back_populates="purchase")

    def __repr__(self):
        return f"<Purchase(id={self.id}, supplier_id={self.supplier_id}, total={self.total})>"
