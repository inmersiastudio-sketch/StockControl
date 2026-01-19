"""
Endpoints de Productos
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import date, timedelta

from app.db.session import get_db
from app.core.security import get_current_user, get_current_admin
from app.core.config import settings
from app.models.user import User
from app.models.product import Product
from app.models.product_lot import ProductLot
from app.models.category import Category
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductWithLots, ProductLotResponse
)

router = APIRouter()


def get_product_response(product: Product, db: Session) -> ProductResponse:
    """Construir respuesta de producto con datos calculados"""
    # Calcular stock total
    current_stock = sum(lot.quantity for lot in product.lots if lot.quantity > 0)
    
    # Obtener próximo vencimiento
    next_exp = None
    for lot in sorted(product.lots, key=lambda x: x.expiration_date or date.max):
        if lot.quantity > 0 and lot.expiration_date:
            next_exp = lot.expiration_date
            break
    
    # Obtener nombre de categoría
    category_name = product.category.name if product.category else None
    
    # Calcular margen
    margin = 0
    if product.price > 0 and product.cost > 0:
        margin = ((product.price - product.cost) / product.price) * 100
    
    return ProductResponse(
        id=product.id,
        code=product.code,
        barcode=product.barcode,
        name=product.name,
        description=product.description,
        category_id=product.category_id,
        category_name=category_name,
        cost=product.cost,
        price=product.price,
        min_stock=product.min_stock,
        current_stock=current_stock,
        margin_percentage=round(margin, 2),
        is_active=product.is_active,
        created_at=product.created_at,
        next_expiration=next_exp
    )


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    low_stock: bool = False,
    expiring_soon: bool = False,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listar productos con filtros
    """
    query = db.query(Product)
    
    # Filtro por activo
    if active_only:
        query = query.filter(Product.is_active == True)
    
    # Búsqueda por nombre o código
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.code.ilike(search_term),
                Product.barcode.ilike(search_term)
            )
        )
    
    # Filtro por categoría
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    products = query.offset(skip).limit(limit).all()
    
    result = []
    for p in products:
        prod_response = get_product_response(p, db)
        
        # Filtro por stock bajo
        if low_stock and prod_response.current_stock >= p.min_stock:
            continue
        
        # Filtro por próximos a vencer
        if expiring_soon:
            if not prod_response.next_expiration:
                continue
            days_until_exp = (prod_response.next_expiration - date.today()).days
            if days_until_exp > settings.EXPIRATION_ALERT_DAYS:
                continue
        
        result.append(prod_response)
    
    return result


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Crear un producto (Solo Admin)
    """
    # Verificar código único
    existing = db.query(Product).filter(Product.code == product_data.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un producto con el código '{product_data.code}'"
        )
    
    # Verificar categoría
    if product_data.category_id:
        category = db.query(Category).filter(Category.id == product_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoría no encontrada"
            )
    
    new_product = Product(
        code=product_data.code,
        barcode=product_data.barcode,
        name=product_data.name,
        description=product_data.description,
        category_id=product_data.category_id,
        cost=product_data.cost,
        price=product_data.price,
        min_stock=product_data.min_stock,
        is_active=True
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return get_product_response(new_product, db)


@router.get("/{product_id}", response_model=ProductWithLots)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener un producto con sus lotes
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    base_response = get_product_response(product, db)
    
    # Agregar lotes
    lots = []
    for lot in product.lots:
        if lot.quantity > 0:
            lot_response = ProductLotResponse(
                id=lot.id,
                quantity=lot.quantity,
                initial_quantity=lot.initial_quantity,
                cost=lot.cost,
                expiration_date=lot.expiration_date,
                created_at=lot.created_at,
                is_expired=lot.is_expired
            )
            lots.append(lot_response)
    
    return ProductWithLots(
        **base_response.model_dump(),
        lots=lots
    )


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Actualizar un producto (Solo Admin)
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Verificar código único si se está actualizando
    if product_data.code:
        existing = db.query(Product).filter(
            Product.code == product_data.code,
            Product.id != product_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe otro producto con el código '{product_data.code}'"
            )
    
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return get_product_response(product, db)


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Eliminar (desactivar) un producto (Solo Admin)
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # No eliminar, solo desactivar
    product.is_active = False
    db.commit()
    
    return {"message": f"Producto '{product.name}' desactivado"}
