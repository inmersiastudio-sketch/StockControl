"""
Endpoints de Ventas
TODO: Implementar lógica completa en Sprint 2
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleResponse

router = APIRouter()


@router.get("/", response_model=List[SaleResponse])
async def list_sales(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listar ventas
    TODO: Implementar en Sprint 2
    """
    return []


@router.post("/", response_model=SaleResponse)
async def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear una venta
    TODO: Implementar en Sprint 2
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo - Sprint 2"
    )
