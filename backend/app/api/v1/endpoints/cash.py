"""
Endpoints de Caja
TODO: Implementar lógica completa en Sprint 6
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.schemas.cash import CashMovementCreate, CashSummary

router = APIRouter()


@router.get("/summary", response_model=CashSummary)
async def get_cash_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Obtener resumen de caja del día (Solo Admin)
    TODO: Implementar en Sprint 6
    """
    return CashSummary(
        date=date.today(),
        sales_cash=0,
        sales_card=0,
        sales_transfer=0,
        additional_incomes=0,
        expenses=0,
        expected_cash=0,
        total_sales=0,
        total_transactions=0
    )


@router.post("/movement")
async def create_cash_movement(
    movement_data: CashMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Registrar movimiento de caja (Solo Admin)
    TODO: Implementar en Sprint 6
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo - Sprint 6"
    )


@router.post("/close")
async def close_cash(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Realizar cierre de caja (Solo Admin)
    TODO: Implementar en Sprint 6
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo - Sprint 6"
    )
