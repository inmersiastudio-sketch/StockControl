"""
StockControl API - Sistema de Inventario Local
Versión: 1.0.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.v1.router import api_router

# Importar todos los modelos para que se registren en Base
from app.models import (
    User, Category, Supplier, Product, ProductLot,
    Purchase, PurchaseItem, Sale, SaleItem,
    CashMovement, CashClosure
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de inicio y cierre de la aplicación"""
    # Startup: crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada")
    yield
    # Shutdown
    print("👋 Cerrando aplicación...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema de gestión de inventario para despensas y almacenes argentinos",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS para permitir conexiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health_check():
    """Endpoint para verificar que el servidor está funcionando"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION
    }
