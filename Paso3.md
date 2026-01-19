## 🚀 PASO 3: ENDPOINTS FASTAPI COMPLETOS

***

## 1. DEPENDENCIES (backend/api/deps.py)

```python
"""
Dependencias para FastAPI (Auth, DB)
"""

from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from core.config import settings
from core.security import verify_password
from db.session import get_db
from models.user import User
from schemas.auth import TokenData

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    Obtener usuario actual desde JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username, role=payload.get("role"))
    
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Validar que el usuario actual sea admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador",
        )
    return current_user


# Type aliases para usar en endpoints
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAdmin = Annotated[User, Depends(get_current_admin)]
DBSession = Annotated[Session, Depends(get_db)]
```

***

## 2. AUTH ENDPOINTS (backend/api/v1/auth.py)

```python
"""
Endpoints de Autenticación
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.deps import get_db, get_current_user
from core.config import settings
from core.security import verify_password, create_access_token
from models.user import User
from schemas.auth import Token, LoginRequest
from schemas.user import User as UserSchema

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login con username y password
    Retorna JWT token
    """
    # Buscar usuario
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar password
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserSchema)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Obtener información del usuario actual
    """
    return current_user
```

***

## 3. USERS ENDPOINTS (backend/api/v1/users.py)

```python
"""
Endpoints de Gestión de Usuarios (Solo Admin)
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import DBSession, CurrentAdmin
from core.security import get_password_hash
from models.user import User
from schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=list[UserSchema])
def list_users(
    db: DBSession,
    current_user: CurrentAdmin,
    skip: int = 0,
    limit: int = 100,
):
    """
    Listar todos los usuarios
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Crear nuevo usuario (empleado o admin)
    """
    # Verificar que el username no exista
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe",
        )
    
    # Validar role
    if user_in.role not in ["admin", "employee"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol inválido. Debe ser 'admin' o 'employee'",
        )
    
    # Crear usuario
    user = User(
        username=user_in.username,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role,
        is_active=True,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Actualizar usuario
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    # Actualizar campos
    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    
    if user_in.password is not None:
        user.password_hash = get_password_hash(user_in.password)
    
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Eliminar usuario (solo si no tiene ventas)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    # No permitir eliminar si tiene ventas
    if user.sales:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un usuario con ventas registradas. Desactívalo en su lugar.",
        )
    
    # No permitir eliminarse a sí mismo
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propio usuario",
        )
    
    db.delete(user)
    db.commit()
    
    return None
```

***

## 4. CATEGORIES ENDPOINTS (backend/api/v1/categories.py)

```python
"""
Endpoints de Categorías
"""

from fastapi import APIRouter, HTTPException, status

from api.deps import DBSession, CurrentAdmin
from models.category import Category
from schemas.category import Category as CategorySchema, CategoryCreate

router = APIRouter()


@router.get("/", response_model=list[CategorySchema])
def list_categories(db: DBSession):
    """
    Listar todas las categorías (sin autenticación requerida)
    """
    categories = db.query(Category).order_by(Category.name).all()
    return categories


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Crear nueva categoría (solo admin)
    """
    # Verificar que no exista
    existing = db.query(Category).filter(Category.name == category_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría ya existe",
        )
    
    category = Category(name=category_in.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Eliminar categoría (solo si no tiene productos)
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    
    # Verificar que no tenga productos
    if category.products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. Hay {len(category.products)} productos en esta categoría",
        )
    
    db.delete(category)
    db.commit()
    
    return None
```

***

## 5. PRODUCTS ENDPOINTS (backend/api/v1/products.py)

```python
"""
Endpoints de Productos
"""

from fastapi import APIRouter, HTTPException, status, Query

from api.deps import DBSession, CurrentUser, CurrentAdmin
from models.product import Product
from models.category import Category
from schemas.product import (
    Product as ProductSchema,
    ProductCreate,
    ProductUpdate,
    ProductWithStock,
)

router = APIRouter()


@router.get("/", response_model=list[ProductWithStock])
def list_products(
    db: DBSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    category_id: int | None = None,
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
            (Product.name.ilike(f"%{search}%")) |
            (Product.code.ilike(f"%{search}%"))
        )
    
    # Filtro por categoría
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    # Filtro activos
    if active_only:
        query = query.filter(Product.is_active == True)
    
    products = query.offset(skip).limit(limit).all()
    
    # Filtro stock bajo (después de query porque usa property)
    if low_stock_only:
        products = [p for p in products if p.current_stock < p.min_stock]
    
    return products


@router.get("/{product_id}", response_model=ProductWithStock)
def get_product(
    product_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Obtener producto por ID
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return product


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
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
    
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product


@router.put("/{product_id}", response_model=ProductSchema)
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
    if "category_id" in update_data:
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
    
    return product


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
    if product.current_stock > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. Tiene {product.current_stock} unidades en stock",
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


@router.get("/alerts/low-stock", response_model=list[ProductWithStock])
def get_low_stock_products(
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Obtener productos con stock bajo
    """
    products = db.query(Product).filter(Product.is_active == True).all()
    low_stock = [p for p in products if p.current_stock < p.min_stock]
    return low_stock


@router.get("/alerts/expiring-soon", response_model=list[ProductWithStock])
def get_expiring_products(
    db: DBSession,
    current_user: CurrentUser,
    days: int = Query(default=7, ge=1, le=30),
):
    """
    Obtener productos próximos a vencer
    """
    from datetime import date, timedelta
    
    products = db.query(Product).filter(Product.is_active == True).all()
    expiring = []
    
    for product in products:
        if product.next_expiration_date:
            days_until = (product.next_expiration_date - date.today()).days
            if 0 <= days_until <= days:
                expiring.append(product)
    
    # Ordenar por fecha de vencimiento
    expiring.sort(key=lambda p: p.next_expiration_date)
    
    return expiring
```

***

## 6. SUPPLIERS ENDPOINTS (backend/api/v1/suppliers.py)

```python
"""
Endpoints de Proveedores
"""

from fastapi import APIRouter, HTTPException, status

from api.deps import DBSession, CurrentAdmin
from models.supplier import Supplier
from schemas.supplier import (
    Supplier as SupplierSchema,
    SupplierCreate,
    SupplierUpdate,
)

router = APIRouter()


@router.get("/", response_model=list[SupplierSchema])
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


@router.get("/{supplier_id}", response_model=SupplierSchema)
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


@router.post("/", response_model=SupplierSchema, status_code=status.HTTP_201_CREATED)
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
    
    supplier = Supplier(**supplier_in.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    
    return supplier


@router.put("/{supplier_id}", response_model=SupplierSchema)
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
    if "cuit" in update_data and update_data["cuit"] != supplier.cuit:
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
```

***

## 7. SALES ENDPOINTS (backend/api/v1/sales.py)

```python
"""
Endpoints de Ventas
"""

from datetime import date, datetime
from fastapi import APIRouter, HTTPException, status, Query

from api.deps import DBSession, CurrentUser, CurrentAdmin
from models.sale import Sale
from models.sale_item import SaleItem
from models.product import Product
from models.product_lot import ProductLot
from schemas.sale import (
    Sale as SaleSchema,
    SaleCreate,
    SaleWithItems,
    SaleCancel,
)
from core.security import verify_password

router = APIRouter()


def process_sale_fifo(db: DBSession, product_id: int, quantity_needed: int) -> tuple[float, list]:
    """
    Procesar venta usando FIFO y retornar costo promedio
    Retorna: (costo_promedio, lista_de_lotes_actualizados)
    """
    # Obtener lotes ordenados por fecha de vencimiento (FIFO)
    lots = db.query(ProductLot).filter(
        ProductLot.product_id == product_id,
        ProductLot.quantity > 0,
    ).order_by(ProductLot.expiration_date.asc()).all()
    
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


@router.post("/", response_model=SaleWithItems, status_code=status.HTTP_201_CREATED)
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
    total = subtotal - sale_in.discount
    
    if total < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El descuento no puede ser mayor al subtotal",
        )
    
    # Crear venta
    sale = Sale(
        user_id=current_user.id,
        total=total,
        discount=sale_in.discount,
        payment_method=sale_in.payment_method,
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


@router.get("/", response_model=list[SaleWithItems])
def list_sales(
    db: DBSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    date_from: date | None = None,
    date_to: date | None = None,
    user_id: int | None = None,
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
        query = query.filter(Sale.created_at >= date_from)
    if date_to:
        query = query.filter(Sale.created_at <= date_to)
    
    # Filtro de canceladas
    if not include_cancelled:
        query = query.filter(Sale.is_cancelled == False)
    
    sales = query.order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()
    return sales


@router.get("/{sale_id}", response_model=SaleWithItems)
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


@router.post("/{sale_id}/cancel", response_model=SaleWithItems)
def cancel_sale(
    sale_id: int,
    cancel_data: SaleCancel,
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
        from models.user import User
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


@router.get("/stats/today", response_model=dict)
def get_today_stats(
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Estadísticas de ventas del día
    Admin: todas las ventas
    Employee: solo sus ventas
    """
    from sqlalchemy import func
    
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
    total_profit = sum(sale.total_profit for sale in sales)
    
    return {
        "date": today,
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "average_sale": total_revenue / total_sales if total_sales > 0 else 0,
    }
```

***

## 8. ACTUALIZAR main.py con todos los routers

```python
# ... (código anterior)

from api.v1 import (
    auth,
    users,
    categories,
    products,
    suppliers,
    # purchases,  # Lo haremos en siguiente paso
    sales,
    # returns,    # Próximo paso
    # cash,       # Próximo paso
    # reports,    # Próximo paso
    # config,     # Próximo paso
)

# ... (código del lifespan)

# Incluir routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Usuarios"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categorías"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Productos"])
app.include_router(suppliers.router, prefix="/api/v1/suppliers", tags=["Proveedores"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["Ventas"])

# ... (resto del código)
```

***

## 9. TESTING DE LOS ENDPOINTS

### `scripts/test-api.sh`

```bash
#!/bin/bash

echo "🧪 Testing StockControl API"

API_URL="http://localhost:8000/api/v1"

# 1. Login
echo "1️⃣  Testing Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123")

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

if [ "$TOKEN" != "null" ]; then
  echo "✅ Login exitoso"
else
  echo "❌ Login falló"
  exit 1
fi

# 2. Obtener usuario actual
echo ""
echo "2️⃣  Testing Get Current User..."
curl -s -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq

# 3. Listar categorías
echo ""
echo "3️⃣  Testing List Categories..."
curl -s -X GET "$API_URL/categories" | jq

# 4. Listar productos
echo ""
echo "4️⃣  Testing List Products..."
curl -s -X GET "$API_URL/products" \
  -H "Authorization: Bearer $TOKEN" | jq

# 5. Crear venta
echo ""
echo "5️⃣  Testing Create Sale..."
curl -s -X POST "$API_URL/sales" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 3, "quantity": 5}
    ],
    "payment_method": "cash",
    "discount": 0
  }' | jq

echo ""
echo "✅ Tests completados"
```

***

## ✅ CHECKLIST PASO 3 COMPLETADO

- ✅ Dependencies (Auth middleware)
- ✅ Auth endpoints (Login, Get Me)
- ✅ Users endpoints (CRUD completo)
- ✅ Categories endpoints (CRUD)
- ✅ Products endpoints (CRUD + Alertas)
- ✅ Suppliers endpoints (CRUD completo)
- ✅ Sales endpoints (CRUD + FIFO + Cancelar)
- ✅ Script de testing

***

## 🚀 CÓMO PROBAR

```bash
# 1. Iniciar backend
cd backend
source venv/bin/activate
python main.py

# 2. En otra terminal, probar endpoints
# Opción A: Con script
bash scripts/test-api.sh

# Opción B: Manualmente con Swagger UI
# Abrir navegador en: http://localhost:8000/docs
```

***

**Próximo paso:** ¿Querés que te arme el **PASO 4 (Purchases con OCR + Cash + Reports + Config endpoints)?** O preferís que arranquemos con el frontend ya?