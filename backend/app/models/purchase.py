"""
Modelos de Compra (Purchase) y Items de Compra
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Purchase(Base):
    """
    Registro de compra a proveedor.
    Puede incluir datos de OCR si se cargó con foto de ticket.
    """
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    
    # Totales
    total = Column(Float, nullable=False)
    
    # Notas y observaciones
    notes = Column(Text, nullable=True)
    
    # OCR - Foto del ticket
    receipt_image_path = Column(String(500), nullable=True)
    ocr_raw_text = Column(Text, nullable=True)  # Texto extraído por OCR
    ocr_data = Column(JSON, nullable=True)  # Datos estructurados del OCR
    
    # Usuario que registró la compra
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    purchase_date = Column(Date, nullable=True)  # Fecha del ticket
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    supplier = relationship("Supplier", back_populates="purchases")
    user = relationship("User")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")
    lots = relationship("ProductLot", back_populates="purchase")
    
    def __repr__(self):
        return f"<Purchase {self.id}: ${self.total}>"


class PurchaseItem(Base):
    """
    Item individual de una compra.
    Cada item puede generar un lote con fecha de vencimiento.
    """
    __tablename__ = "purchase_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)  # quantity * unit_cost
    
    expiration_date = Column(Date, nullable=True)  # Fecha de vencimiento del lote
    
    # Relaciones
    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product", back_populates="purchase_items")
    
    def __repr__(self):
        return f"<PurchaseItem {self.quantity}x {self.product_id}>"
