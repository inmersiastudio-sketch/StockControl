"""
Schemas de Venta
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    transfer = "transfer"


# --- Items de venta ---

class SaleItemCreate(BaseModel):
    """Item para agregar a una venta"""
    product_id: int
    quantity: int = Field(..., gt=0)


class SaleItemResponse(BaseModel):
    """Respuesta de item de venta"""
    id: int
    product_id: int
    product_name: str = ""
    product_code: str = ""
    quantity: int
    unit_price: float
    unit_cost: float
    subtotal: float
    profit: float = 0
    
    class Config:
        from_attributes = True


# --- Venta completa ---

class SaleCreate(BaseModel):
    """Schema para crear una venta"""
    items: List[SaleItemCreate] = Field(..., min_length=1)
    payment_method: PaymentMethod
    discount: float = Field(default=0, ge=0)
    amount_paid: Optional[float] = None  # Para calcular vuelto


class SaleResponse(BaseModel):
    """Schema de respuesta para venta"""
    id: int
    subtotal: float
    discount: float
    total: float
    payment_method: PaymentMethod
    amount_paid: Optional[float]
    change_given: Optional[float]
    user_id: int
    user_name: str = ""
    is_cancelled: bool
    cancel_reason: Optional[str]
    created_at: datetime
    items: List[SaleItemResponse] = []
    profit: float = 0
    
    class Config:
        from_attributes = True


class SaleCancelRequest(BaseModel):
    """Schema para anular una venta"""
    reason: str = Field(..., min_length=3, max_length=500)
    admin_password: Optional[str] = None  # Si es empleado


# --- Filtros de búsqueda ---

class SaleSearch(BaseModel):
    """Filtros para buscar ventas"""
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    user_id: Optional[int] = None
    payment_method: Optional[PaymentMethod] = None
    include_cancelled: bool = False
