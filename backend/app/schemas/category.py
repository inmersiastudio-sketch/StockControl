"""
Schemas de Categoría
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    """Schema para crear categoría"""
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    """Schema para actualizar categoría"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    """Schema de respuesta para categoría"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    product_count: int = 0  # Cantidad de productos en esta categoría
    
    class Config:
        from_attributes = True
