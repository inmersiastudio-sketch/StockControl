"""
Endpoints de Compras
TODO: Implementar lógica completa en Sprint 4-5
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.schemas.purchase import PurchaseCreate, PurchaseResponse

router = APIRouter()


@router.get("/", response_model=List[PurchaseResponse])
async def list_purchases(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Listar compras (Solo Admin)
    TODO: Implementar en Sprint 4
    """
    return []


@router.post("/", response_model=PurchaseResponse)
async def create_purchase(
    purchase_data: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Crear una compra manual (Solo Admin)
    TODO: Implementar en Sprint 4
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo - Sprint 4"
    )


@router.post("/ocr")
async def create_purchase_from_ocr(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Crear compra desde imagen con OCR (Solo Admin)
    TODO: Implementar en Sprint 5
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo - Sprint 5"
    )
