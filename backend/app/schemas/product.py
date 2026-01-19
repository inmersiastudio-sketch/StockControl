"""
Schemas de Producto
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date


class ProductCreate(BaseModel):
    """Schema para crear producto"""
    code: str = Field(..., min_length=1, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    cost: float = Field(default=0, ge=0)
    price: float = Field(..., gt=0)
    min_stock: int = Field(default=10, ge=0)
    
    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v


class ProductUpdate(BaseModel):
    """Schema para actualizar producto"""
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    cost: Optional[float] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)
    min_stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductLotResponse(BaseModel):
    """Schema de respuesta para un lote"""
    id: int
    quantity: int
    initial_quantity: int
    cost: float
    expiration_date: Optional[date]
    created_at: datetime
    is_expired: bool = False
    
    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    """Schema de respuesta para producto"""
    id: int
    code: str
    barcode: Optional[str]
    name: str
    description: Optional[str]
    category_id: Optional[int]
    category_name: Optional[str] = None
    cost: float
    price: float
    min_stock: int
    current_stock: int = 0
    margin_percentage: float = 0
    is_active: bool
    created_at: datetime
    
    # Información de vencimiento
    next_expiration: Optional[date] = None
    
    class Config:
        from_attributes = True


class ProductWithLots(ProductResponse):
    """Producto con detalle de lotes"""
    lots: List[ProductLotResponse] = []


class ProductSearch(BaseModel):
    """Schema para búsqueda de productos"""
    query: Optional[str] = None
    category_id: Optional[int] = None
    low_stock_only: bool = False
    expiring_soon: bool = False
    active_only: bool = True
