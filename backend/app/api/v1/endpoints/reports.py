"""
Endpoints de Reportes
TODO: Implementar en Sprint 6
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.user import User

router = APIRouter()


@router.get("/daily")
async def get_daily_report(
    report_date: date = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Reporte diario (Solo Admin)
    TODO: Implementar en Sprint 6
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo - Sprint 6"
    )


@router.get("/period")
async def get_period_report(
    date_from: date = None,
    date_to: date = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Reporte por período (Solo Admin)
    TODO: Implementar en Sprint 6
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo - Sprint 6"
    )


@router.get("/alerts")
async def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Obtener alertas (stock bajo, próximos a vencer)
    TODO: Implementar en Sprint 6
    """
    return {
        "low_stock": [],
        "expiring_soon": [],
        "no_movement": []
    }
