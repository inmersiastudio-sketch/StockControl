"""
Endpoints de Ventas
"""

from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import func

from app.api.deps import DBSession, CurrentUser, CurrentAdmin, get_current_user
from app.core.security import verify_password
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.product_lot import ProductLot
from app.models.user import User
from app.schemas.sale import (
    SaleCreate,
    SaleResponse,
    SaleCancelRequest,
)

router = APIRouter()


def process_sale_fifo(db: DBSession, product_id: int, quantity_needed: int) -> tuple:
    """
    Procesar venta usando FIFO y retornar costo promedio
    Retorna: (costo_promedio, lista_de_lotes_actualizados)
    """
    # Obtener lotes ordenados por fecha de vencimiento (FIFO)
    lots = db.query(ProductLot).filter(
        ProductLot.product_id == product_id,
        ProductLot.quantity > 0,
    ).order_by(ProductLot.expiration_date.asc().nullslast()).all()
    
    if not lots:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Producto ID {product_id} sin stock disponible",
        )
    
    # Verificar stock total
    total_stock = sum(lot.quantity for lot in lots)
    if total_stock < quantity_needed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Disponible: {total_stock}, Necesario: {quantity_needed}",
        )
    
    # Descontar de lotes usando FIFO
    remaining = quantity_needed
    total_cost = 0.0
    lots_updated = []
    
    for lot in lots:
        if remaining == 0:
            break
        
        if lot.quantity >= remaining:
            # Este lote tiene suficiente
            total_cost += lot.cost * remaining
            lot.quantity -= remaining
            lots_updated.append(lot)
            remaining = 0
        else:
            # Usar todo este lote y continuar
            total_cost += lot.cost * lot.quantity
            remaining -= lot.quantity
            lots_updated.append(lot)
            lot.quantity = 0
    
    avg_cost = total_cost / quantity_needed
    return avg_cost, lots_updated


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_in: SaleCreate,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Crear nueva venta (todos los usuarios)
    """
    if not sale_in.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La venta debe tener al menos un producto",
        )
    
    # Validar que todos los productos existan y calcular total
    sale_items = []
    subtotal = 0.0
    
    for item_in in sale_in.items:
        product = db.query(Product).filter(Product.id == item_in.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto ID {item_in.product_id} no encontrado",
            )
        
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Producto '{product.name}' está inactivo",
            )
        
        # Procesar FIFO y obtener costo real
        avg_cost, lots_updated = process_sale_fifo(db, product.id, item_in.quantity)
        
        # Crear item de venta
        item_subtotal = product.price * item_in.quantity
        sale_item = SaleItem(
            product_id=product.id,
            quantity=item_in.quantity,
            unit_price=product.price,
            unit_cost=avg_cost,
            subtotal=item_subtotal,
        )
        sale_items.append(sale_item)
        subtotal += item_subtotal
    
    # Aplicar descuento
    discount = sale_in.discount if sale_in.discount else 0
    total = subtotal - discount
    
    if total < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El descuento no puede ser mayor al subtotal",
        )
    
    # Crear venta
    sale = Sale(
        user_id=current_user.id,
        subtotal=subtotal,
        total=total,
        discount=discount,
        payment_method=sale_in.payment_method.value if hasattr(sale_in.payment_method, 'value') else sale_in.payment_method,
        amount_paid=sale_in.amount_paid,
        change_given=(sale_in.amount_paid - total) if sale_in.amount_paid and sale_in.amount_paid > total else 0,
    )
    db.add(sale)
    db.flush()  # Para obtener el ID
    
    # Asociar items
    for item in sale_items:
        item.sale_id = sale.id
        db.add(item)
    
    db.commit()
    db.refresh(sale)
    
    return sale


@router.get("/", response_model=List[SaleResponse])
def list_sales(
    db: DBSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    user_id: Optional[int] = None,
    include_cancelled: bool = False,
):
    """
    Listar ventas con filtros
    Admin: ve todas
    Employee: solo sus ventas
    """
    query = db.query(Sale)
    
    # Si es empleado, solo sus ventas
    if current_user.role == "employee":
        query = query.filter(Sale.user_id == current_user.id)
    
    # Si es admin y especifica user_id
    if current_user.role == "admin" and user_id:
        query = query.filter(Sale.user_id == user_id)
    
    # Filtro de fecha
    if date_from:
        query = query.filter(func.date(Sale.created_at) >= date_from)
    if date_to:
        query = query.filter(func.date(Sale.created_at) <= date_to)
    
    # Filtro de canceladas
    if not include_cancelled:
        query = query.filter(Sale.is_cancelled == False)
    
    sales = query.order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()
    return sales


@router.get("/stats/today")
def get_today_stats(
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Estadísticas de ventas del día
    Admin: todas las ventas
    Employee: solo sus ventas
    """
    today = date.today()
    query = db.query(Sale).filter(
        func.date(Sale.created_at) == today,
        Sale.is_cancelled == False,
    )
    
    # Filtrar por empleado si no es admin
    if current_user.role == "employee":
        query = query.filter(Sale.user_id == current_user.id)
    
    sales = query.all()
    
    total_sales = len(sales)
    total_revenue = sum(sale.total for sale in sales)
    
    # Calcular ganancia total
    total_profit = 0.0
    for sale in sales:
        for item in sale.items:
            profit = (item.unit_price - item.unit_cost) * item.quantity
            total_profit += profit
    
    return {
        "date": str(today),
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "total_profit": round(total_profit, 2),
        "average_sale": round(total_revenue / total_sales, 2) if total_sales > 0 else 0,
    }


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Obtener venta por ID
    """
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada",
        )
    
    # Empleados solo pueden ver sus ventas
    if current_user.role == "employee" and sale.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta venta",
        )
    
    return sale


@router.post("/{sale_id}/cancel", response_model=SaleResponse)
def cancel_sale(
    sale_id: int,
    cancel_data: SaleCancelRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Anular venta (reintegrar stock)
    Admin: puede anular cualquiera
    Employee: solo del mismo día y con contraseña admin
    """
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada",
        )
    
    if sale.is_cancelled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La venta ya está anulada",
        )
    
    # Verificar que sea del mismo día
    sale_date = sale.created_at.date()
    if sale_date != date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden anular ventas del mismo día",
        )
    
    # Si es empleado, validar contraseña admin
    if current_user.role == "employee":
        if not cancel_data.admin_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se requiere contraseña de administrador",
            )
        
        # Buscar cualquier admin activo
        admin = db.query(User).filter(
            User.role == "admin",
            User.is_active == True,
        ).first()
        
        if not admin or not verify_password(cancel_data.admin_password, admin.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña de administrador incorrecta",
            )
    
    # Reintegrar stock a lotes (FIFO reverso)
    for item in sale.items:
        # Buscar el lote más antiguo del producto para reintegrar
        lot = db.query(ProductLot).filter(
            ProductLot.product_id == item.product_id,
        ).order_by(ProductLot.created_at.asc()).first()
        
        if lot:
            lot.quantity += item.quantity
        else:
            # Si no hay lotes, crear uno nuevo
            new_lot = ProductLot(
                product_id=item.product_id,
                quantity=item.quantity,
                initial_quantity=item.quantity,
                cost=item.unit_cost,
            )
            db.add(new_lot)
    
    # Marcar venta como cancelada
    sale.is_cancelled = True
    sale.cancelled_at = datetime.utcnow()
    sale.cancelled_by = current_user.id
    sale.cancel_reason = cancel_data.reason
    
    db.commit()
    db.refresh(sale)
    
    return sale
