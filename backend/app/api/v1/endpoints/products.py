"""
Endpoints de Productos
"""

from typing import List, Optional
from datetime import date, timedelta
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import or_

from app.api.deps import DBSession, CurrentUser, CurrentAdmin
from app.models.product import Product
from app.models.product_lot import ProductLot
from app.models.category import Category
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductWithLots,
    ProductLotResponse,
)

router = APIRouter()


def get_product_response(product: Product) -> ProductResponse:
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
def list_products(
    db: DBSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    active_only: bool = True,
    low_stock_only: bool = False,
):
    """
    Listar productos con filtros
    """
    query = db.query(Product)
    
    # Filtro de búsqueda
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.code.ilike(f"%{search}%")
            )
        )
    
    # Filtro por categoría
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    # Filtro activos
    if active_only:
        query = query.filter(Product.is_active == True)
    
    products = query.offset(skip).limit(limit).all()
    
    result = [get_product_response(p) for p in products]
    
    # Filtro stock bajo (después de query porque usa property)
    if low_stock_only:
        result = [p for p in result if p.current_stock < p.min_stock]
    
    return result


@router.get("/alerts/low-stock", response_model=List[ProductResponse])
def get_low_stock_products(
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Obtener productos con stock bajo
    """
    products = db.query(Product).filter(Product.is_active == True).all()
    result = []
    for p in products:
        prod_response = get_product_response(p)
        if prod_response.current_stock < p.min_stock:
            result.append(prod_response)
    return result


@router.get("/alerts/expiring-soon", response_model=List[ProductResponse])
def get_expiring_products(
    db: DBSession,
    current_user: CurrentUser,
    days: int = Query(default=7, ge=1, le=30),
):
    """
    Obtener productos próximos a vencer
    """
    products = db.query(Product).filter(Product.is_active == True).all()
    expiring = []
    
    for product in products:
        prod_response = get_product_response(product)
        if prod_response.next_expiration:
            days_until = (prod_response.next_expiration - date.today()).days
            if 0 <= days_until <= days:
                expiring.append(prod_response)
    
    # Ordenar por fecha de vencimiento
    expiring.sort(key=lambda p: p.next_expiration)
    
    return expiring


@router.get("/{product_id}", response_model=ProductWithLots)
def get_product(
    product_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Obtener producto por ID con sus lotes
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    
    base_response = get_product_response(product)
    
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
                is_expired=lot.is_expired if hasattr(lot, 'is_expired') else False
            )
            lots.append(lot_response)
    
    return ProductWithLots(
        **base_response.model_dump(),
        lots=lots
    )


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Crear nuevo producto (solo admin)
    """
    # Verificar que el código no exista
    existing = db.query(Product).filter(Product.code == product_in.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código de producto ya existe",
        )
    
    # Verificar que la categoría exista
    if product_in.category_id:
        category = db.query(Category).filter(Category.id == product_in.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )
    
    # Validar precio > costo
    if product_in.price <= product_in.cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio de venta debe ser mayor al costo",
        )
    
    product = Product(
        code=product_in.code,
        barcode=getattr(product_in, 'barcode', None),
        name=product_in.name,
        description=getattr(product_in, 'description', None),
        category_id=product_in.category_id,
        cost=product_in.cost,
        price=product_in.price,
        min_stock=product_in.min_stock,
        is_active=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return get_product_response(product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Actualizar producto (solo admin)
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    
    # Actualizar campos
    update_data = product_in.model_dump(exclude_unset=True)
    
    # Validar código único si se cambia
    if "code" in update_data and update_data["code"] != product.code:
        existing = db.query(Product).filter(Product.code == update_data["code"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de producto ya existe",
            )
    
    # Validar categoría si se cambia
    if "category_id" in update_data and update_data["category_id"]:
        category = db.query(Category).filter(Category.id == update_data["category_id"]).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )
    
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return get_product_response(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Eliminar producto (solo si no tiene stock ni ventas)
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    
    # Verificar que no tenga stock
    current_stock = sum(lot.quantity for lot in product.lots if lot.quantity > 0)
    if current_stock > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. Tiene {current_stock} unidades en stock",
        )
    
    # Verificar que no tenga ventas
    if product.sale_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un producto con ventas registradas. Desactívalo en su lugar.",
        )
    
    db.delete(product)
    db.commit()
    
    return None
