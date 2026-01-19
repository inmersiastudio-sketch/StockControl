"""
Modelo de Proveedor
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    cuit = Column(String(20), nullable=True)  # Formato: XX-XXXXXXXX-X
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con compras
    purchases = relationship("Purchase", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier {self.name}>"


# Importar Boolean que faltó
from sqlalchemy import Boolean
