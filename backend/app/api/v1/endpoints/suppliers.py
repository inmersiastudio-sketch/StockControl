"""
Endpoints de Proveedores
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.db.session import get_db
from app.core.security import get_current_user, get_current_admin
from app.models.user import User
from app.models.supplier import Supplier
from app.models.purchase import Purchase
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse

router = APIRouter()


@router.get("/", response_model=List[SupplierResponse])
async def list_suppliers(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Listar proveedores (Solo Admin)
    """
    query = db.query(Supplier)
    
    if active_only:
        query = query.filter(Supplier.is_active == True)
    
    suppliers = query.offset(skip).limit(limit).all()
    
    result = []
    for sup in suppliers:
        # Calcular estadísticas
        purchases = db.query(Purchase).filter(Purchase.supplier_id == sup.id).all()
        total_purchases = len(purchases)
        total_spent = sum(p.total for p in purchases)
        
        sup_response = SupplierResponse(
            id=sup.id,
            name=sup.name,
            cuit=sup.cuit,
            phone=sup.phone,
            email=sup.email,
            address=sup.address,
            notes=sup.notes,
            is_active=sup.is_active,
            created_at=sup.created_at,
            total_purchases=total_purchases,
            total_spent=total_spent
        )
        result.append(sup_response)
    
    return result


@router.post("/", response_model=SupplierResponse)
async def create_supplier(
    supplier_data: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Crear un proveedor (Solo Admin)
    """
    new_supplier = Supplier(
        name=supplier_data.name,
        cuit=supplier_data.cuit,
        phone=supplier_data.phone,
        email=supplier_data.email,
        address=supplier_data.address,
        notes=supplier_data.notes,
        is_active=True
    )
    
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    
    return SupplierResponse(
        id=new_supplier.id,
        name=new_supplier.name,
        cuit=new_supplier.cuit,
        phone=new_supplier.phone,
        email=new_supplier.email,
        address=new_supplier.address,
        notes=new_supplier.notes,
        is_active=new_supplier.is_active,
        created_at=new_supplier.created_at,
        total_purchases=0,
        total_spent=0
    )


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Obtener un proveedor por ID (Solo Admin)
    """
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    
    # Calcular estadísticas
    purchases = db.query(Purchase).filter(Purchase.supplier_id == supplier.id).all()
    
    return SupplierResponse(
        id=supplier.id,
        name=supplier.name,
        cuit=supplier.cuit,
        phone=supplier.phone,
        email=supplier.email,
        address=supplier.address,
        notes=supplier.notes,
        is_active=supplier.is_active,
        created_at=supplier.created_at,
        total_purchases=len(purchases),
        total_spent=sum(p.total for p in purchases)
    )


@router.patch("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Actualizar un proveedor (Solo Admin)
    """
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    
    update_data = supplier_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.commit()
    db.refresh(supplier)
    
    # Calcular estadísticas
    purchases = db.query(Purchase).filter(Purchase.supplier_id == supplier.id).all()
    
    return SupplierResponse(
        id=supplier.id,
        name=supplier.name,
        cuit=supplier.cuit,
        phone=supplier.phone,
        email=supplier.email,
        address=supplier.address,
        notes=supplier.notes,
        is_active=supplier.is_active,
        created_at=supplier.created_at,
        total_purchases=len(purchases),
        total_spent=sum(p.total for p in purchases)
    )


@router.delete("/{supplier_id}")
async def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Eliminar (desactivar) un proveedor (Solo Admin)
    """
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    
    supplier.is_active = False
    db.commit()
    
    return {"message": f"Proveedor '{supplier.name}' desactivado"}
