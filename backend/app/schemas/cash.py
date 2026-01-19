"""
Schemas de Caja
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime, date
from enum import Enum


class MovementType(str, Enum):
    income = "income"
    expense = "expense"


class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    transfer = "transfer"


# --- Movimientos de caja ---

class CashMovementCreate(BaseModel):
    """Schema para crear un movimiento de caja"""
    type: MovementType
    amount: float = Field(..., gt=0)
    method: PaymentMethod
    description: str = Field(..., min_length=3, max_length=500)


class CashMovementResponse(BaseModel):
    """Respuesta de movimiento de caja"""
    id: int
    type: MovementType
    amount: float
    method: PaymentMethod
    description: str
    user_id: int
    user_name: str = ""
    created_at: datetime
    
    class Config:
        from_attributes = True


# --- Cierre de caja ---

class BillsCount(BaseModel):
    """Conteo de billetes para arqueo"""
    b1000: int = 0  # Billetes de $1000
    b500: int = 0
    b200: int = 0
    b100: int = 0
    b50: int = 0
    b20: int = 0
    b10: int = 0
    coins: float = 0  # Monedas (total)


class CashClosureCreate(BaseModel):
    """Schema para crear cierre de caja"""
    counted_cash: float = Field(..., ge=0)
    bills_count: Optional[BillsCount] = None
    notes: Optional[str] = None


class CashClosureResponse(BaseModel):
    """Respuesta de cierre de caja"""
    id: int
    date: date
    expected_cash: float
    counted_cash: float
    difference: float
    bills_count: Optional[Dict] = None
    total_sales_cash: float
    total_sales_card: float
    total_sales_transfer: float
    total_incomes: float
    total_expenses: float
    notes: Optional[str]
    user_id: int
    user_name: str = ""
    created_at: datetime
    
    class Config:
        from_attributes = True


# --- Resumen de caja ---

class CashSummary(BaseModel):
    """Resumen actual de caja (antes del cierre)"""
    date: date
    sales_cash: float = 0
    sales_card: float = 0
    sales_transfer: float = 0
    additional_incomes: float = 0
    expenses: float = 0
    expected_cash: float = 0
    total_sales: float = 0
    total_transactions: int = 0
