"""
Endpoints de Proveedores
"""

from typing import List
from fastapi import APIRouter, HTTPException, status

from app.api.deps import DBSession, CurrentAdmin
from app.models.supplier import Supplier
from app.schemas.supplier import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
)

router = APIRouter()


@router.get("/", response_model=List[SupplierResponse])
def list_suppliers(
    db: DBSession,
    current_user: CurrentAdmin,
    skip: int = 0,
    limit: int = 100,
):
    """
    Listar todos los proveedores
    """
    suppliers = db.query(Supplier).order_by(Supplier.name).offset(skip).limit(limit).all()
    return suppliers


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Obtener proveedor por ID
    """
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )
    return supplier


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier_in: SupplierCreate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Crear nuevo proveedor
    """
    # Verificar CUIT único si se proporciona
    if supplier_in.cuit:
        existing = db.query(Supplier).filter(Supplier.cuit == supplier_in.cuit).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un proveedor con ese CUIT",
            )
    
    supplier = Supplier(
        name=supplier_in.name,
        cuit=supplier_in.cuit,
        phone=supplier_in.phone,
        email=supplier_in.email,
        address=supplier_in.address,
        notes=getattr(supplier_in, 'notes', None),
        is_active=True
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    
    return supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier_in: SupplierUpdate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Actualizar proveedor
    """
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )
    
    update_data = supplier_in.model_dump(exclude_unset=True)
    
    # Validar CUIT único si se cambia
    if "cuit" in update_data and update_data["cuit"] and update_data["cuit"] != supplier.cuit:
        existing = db.query(Supplier).filter(Supplier.cuit == update_data["cuit"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un proveedor con ese CUIT",
            )
    
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.commit()
    db.refresh(supplier)
    
    return supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Eliminar proveedor (solo si no tiene compras)
    """
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )
    
    # Verificar que no tenga compras
    if supplier.purchases:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. Tiene {len(supplier.purchases)} compras registradas",
        )
    
    db.delete(supplier)
    db.commit()
    
    return None
