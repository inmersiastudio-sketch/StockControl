"""
Schemas de Reportes
"""
from typing import Optional, Dict
from pydantic import BaseModel
from datetime import date


class DailySummary(BaseModel):
    """Resumen diario"""
    date: date
    total_sales: int
    total_revenue: float
    total_profit: float
    average_margin: float
    sales_by_payment: Dict[str, float]


class TopProduct(BaseModel):
    """Top producto"""
    product_id: int
    product_name: str
    quantity_sold: int
    total_revenue: float
    total_profit: float


class AlertProduct(BaseModel):
    """Producto en alerta"""
    product_id: int
    product_name: str
    current_stock: int
    min_stock: int
    next_expiration: Optional[date]
    days_until_expiration: Optional[int]
