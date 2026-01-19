"""
Schemas de Proveedor
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class SupplierCreate(BaseModel):
    """Schema para crear proveedor"""
    name: str = Field(..., min_length=2, max_length=200)
    cuit: Optional[str] = Field(None, pattern=r"^\d{2}-\d{8}-\d$")
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class SupplierUpdate(BaseModel):
    """Schema para actualizar proveedor"""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    cuit: Optional[str] = Field(None, pattern=r"^\d{2}-\d{8}-\d$")
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierResponse(BaseModel):
    """Schema de respuesta para proveedor"""
    id: int
    name: str
    cuit: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    total_purchases: int = 0  # Cantidad de compras
    total_spent: float = 0  # Total gastado
    
    class Config:
        from_attributes = True
