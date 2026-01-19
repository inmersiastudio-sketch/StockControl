"""
Router principal de la API v1
Agrupa todos los endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, categories, products, suppliers, sales, purchases, cash, reports

api_router = APIRouter()

# Autenticación
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticación"]
)

# Usuarios
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Usuarios"]
)

# Categorías
api_router.include_router(
    categories.router,
    prefix="/categories",
    tags=["Categorías"]
)

# Productos
api_router.include_router(
    products.router,
    prefix="/products",
    tags=["Productos"]
)

# Proveedores
api_router.include_router(
    suppliers.router,
    prefix="/suppliers",
    tags=["Proveedores"]
)

# Ventas
api_router.include_router(
    sales.router,
    prefix="/sales",
    tags=["Ventas"]
)

# Compras
api_router.include_router(
    purchases.router,
    prefix="/purchases",
    tags=["Compras"]
)

# Caja
api_router.include_router(
    cash.router,
    prefix="/cash",
    tags=["Caja"]
)

# Reportes
api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reportes"]
)
