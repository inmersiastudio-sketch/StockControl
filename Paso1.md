## 📁 PASO 1: ESTRUCTURA COMPLETA DEL PROYECTO

```bash
StockControl/
│
├── README.md                           # Documentación principal
├── .gitignore                          # Ignorar node_modules, __pycache__, etc.
├── docker-compose.yml                  # Para desarrollo (opcional)
│
├── docs/                               # Documentación
│   ├── PRD.md                         # Product Requirements Document
│   ├── API.md                         # Documentación de endpoints
│   ├── DATABASE.md                    # Schema de base de datos
│   ├── DEPLOYMENT.md                  # Guía de empaquetado
│   └── USER_MANUAL.md                 # Manual de usuario
│
├── backend/                            # API Python FastAPI
│   ├── .env.example                   # Variables de entorno ejemplo
│   ├── .gitignore
│   ├── requirements.txt               # Dependencias Python
│   ├── requirements-dev.txt           # Dependencias de desarrollo
│   ├── build.spec                     # PyInstaller config
│   ├── main.py                        # Entry point
│   ├── config.py                      # Configuración general
│   │
│   ├── api/                           # Endpoints
│   │   ├── __init__.py
│   │   ├── deps.py                   # Dependencias (auth, DB)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py               # Login, JWT
│   │       ├── users.py              # Gestión de empleados
│   │       ├── categories.py         # Categorías
│   │       ├── products.py           # CRUD productos
│   │       ├── suppliers.py          # CRUD proveedores
│   │       ├── purchases.py          # Compras + OCR
│   │       ├── sales.py              # Ventas
│   │       ├── returns.py            # Devoluciones
│   │       ├── cash.py               # Caja
│   │       ├── reports.py            # Reportes
│   │       └── config.py             # Configuración
│   │
│   ├── core/                          # Lógica central
│   │   ├── __init__.py
│   │   ├── security.py               # Password hashing, JWT
│   │   ├── config.py                 # Settings con Pydantic
│   │   └── constants.py              # Constantes globales
│   │
│   ├── db/                            # Base de datos
│   │   ├── __init__.py
│   │   ├── session.py                # SQLAlchemy session
│   │   ├── base.py                   # Base para modelos
│   │   ├── init_db.py                # Inicializar DB
│   │   └── migrations/               # Alembic (opcional)
│   │
│   ├── models/                        # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── supplier.py
│   │   ├── product.py
│   │   ├── product_lot.py           # Para FIFO
│   │   ├── purchase.py
│   │   ├── purchase_item.py
│   │   ├── sale.py
│   │   ├── sale_item.py
│   │   ├── cash_movement.py
│   │   └── cash_closure.py
│   │
│   ├── schemas/                       # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── supplier.py
│   │   ├── product.py
│   │   ├── purchase.py
│   │   ├── sale.py
│   │   ├── cash.py
│   │   └── report.py
│   │
│   ├── services/                      # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── sale_service.py
│   │   ├── fifo_service.py           # Lógica FIFO
│   │   ├── ocr_service.py            # ⭐ OCR de tickets
│   │   ├── product_matcher.py        # ⭐ Matching productos
│   │   ├── report_service.py
│   │   └── backup_service.py
│   │
│   ├── utils/                         # Utilidades
│   │   ├── __init__.py
│   │   ├── image_processing.py       # Pre-procesamiento OCR
│   │   ├── pdf_generator.py          # Generar PDFs
│   │   └── validators.py             # Validaciones custom
│   │
│   └── data/                          # Datos locales
│       ├── stockcontrol.db           # Base de datos SQLite (gitignore)
│       ├── backups/                  # Backups automáticos
│       ├── receipts/                 # Fotos de tickets
│       └── exports/                  # PDFs/Excel generados
│
├── frontend/                          # Next.js App
│   ├── .env.local.example
│   ├── .gitignore
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── components.json               # shadcn/ui config
│   ├── postcss.config.js
│   │
│   ├── public/
│   │   ├── icon.png
│   │   └── logo.svg
│   │
│   ├── src/
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── layout.tsx           # Root layout
│   │   │   ├── page.tsx             # Redirect a /login
│   │   │   ├── globals.css
│   │   │   │
│   │   │   ├── (auth)/              # Auth routes
│   │   │   │   ├── layout.tsx       # Simple layout sin sidebar
│   │   │   │   └── login/
│   │   │   │       └── page.tsx     # Pantalla de login
│   │   │   │
│   │   │   └── (dashboard)/         # Protected routes
│   │   │       ├── layout.tsx       # Layout con sidebar + header
│   │   │       │
│   │   │       ├── ventas/          # 🛒 Ventas
│   │   │       │   └── page.tsx
│   │   │       │
│   │   │       ├── devoluciones/    # 🔄 Devoluciones
│   │   │       │   └── page.tsx
│   │   │       │
│   │   │       ├── stock/           # 📦 Consulta Stock
│   │   │       │   └── page.tsx
│   │   │       │
│   │   │       ├── productos/       # 📦 Gestión Productos (Admin)
│   │   │       │   ├── page.tsx     # Lista + CRUD
│   │   │       │   └── [id]/
│   │   │       │       └── page.tsx # Editar producto
│   │   │       │
│   │   │       ├── compras/         # 🛍️ Compras + OCR (Admin)
│   │   │       │   ├── page.tsx
│   │   │       │   └── ocr/
│   │   │       │       └── page.tsx # Escanear ticket
│   │   │       │
│   │   │       ├── proveedores/     # 👥 Proveedores (Admin)
│   │   │       │   └── page.tsx
│   │   │       │
│   │   │       ├── caja/            # 💰 Caja (Admin)
│   │   │       │   ├── page.tsx
│   │   │       │   └── cierre/
│   │   │       │       └── page.tsx # Cierre de caja
│   │   │       │
│   │   │       ├── reportes/        # 📊 Reportes (Admin)
│   │   │       │   └── page.tsx
│   │   │       │
│   │   │       └── configuracion/   # ⚙️ Configuración (Admin)
│   │   │           └── page.tsx
│   │   │
│   │   ├── components/              # Componentes React
│   │   │   ├── ui/                  # shadcn/ui components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── dropdown-menu.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   ├── badge.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   └── ... (resto de shadcn)
│   │   │   │
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx       # Header con usuario + logout
│   │   │   │   ├── Sidebar.tsx      # Sidebar navegación
│   │   │   │   └── PageBanner.tsx   # Banner superior secciones
│   │   │   │
│   │   │   ├── ventas/
│   │   │   │   ├── SearchProduct.tsx
│   │   │   │   ├── ProductCard.tsx
│   │   │   │   ├── Cart.tsx
│   │   │   │   ├── PaymentMethod.tsx
│   │   │   │   └── ChangeCalculator.tsx
│   │   │   │
│   │   │   ├── productos/
│   │   │   │   ├── ProductTable.tsx
│   │   │   │   ├── ProductForm.tsx
│   │   │   │   └── MarginIndicator.tsx
│   │   │   │
│   │   │   ├── compras/
│   │   │   │   ├── ManualPurchase.tsx
│   │   │   │   ├── OCRScanner.tsx   # ⭐ Componente cámara
│   │   │   │   ├── OCRReview.tsx    # ⭐ Revisar productos OCR
│   │   │   │   └── ProductMatcher.tsx # ⭐ Matching manual
│   │   │   │
│   │   │   ├── stock/
│   │   │   │   ├── StockTable.tsx
│   │   │   │   ├── StockFilters.tsx
│   │   │   │   └── AlertBanner.tsx
│   │   │   │
│   │   │   ├── caja/
│   │   │   │   ├── CashSummary.tsx
│   │   │   │   ├── MovementForm.tsx
│   │   │   │   ├── MovementHistory.tsx
│   │   │   │   └── CashClosureForm.tsx
│   │   │   │
│   │   │   ├── reportes/
│   │   │   │   ├── DailySummary.tsx
│   │   │   │   ├── SalesChart.tsx
│   │   │   │   ├── TopProducts.tsx
│   │   │   │   └── AlertsWidget.tsx
│   │   │   │
│   │   │   └── shared/
│   │   │       ├── LoadingSpinner.tsx
│   │   │       ├── EmptyState.tsx
│   │   │       ├── ConfirmDialog.tsx
│   │   │       └── Toast.tsx
│   │   │
│   │   ├── hooks/                   # Custom hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useProducts.ts
│   │   │   ├── useSales.ts
│   │   │   ├── usePurchases.ts
│   │   │   ├── useOCR.ts            # ⭐ Hook para OCR
│   │   │   ├── useCash.ts
│   │   │   └── useReports.ts
│   │   │
│   │   ├── lib/                     # Utilities
│   │   │   ├── api.ts               # Axios/fetch wrapper
│   │   │   ├── auth.ts              # JWT handling
│   │   │   ├── utils.ts             # Helpers (cn, formatters)
│   │   │   └── constants.ts         # Constantes frontend
│   │   │
│   │   ├── store/                   # Zustand stores
│   │   │   ├── authStore.ts
│   │   │   ├── cartStore.ts
│   │   │   └── configStore.ts
│   │   │
│   │   └── types/                   # TypeScript types
│   │       ├── index.ts
│   │       ├── user.ts
│   │       ├── product.ts
│   │       ├── sale.ts
│   │       ├── purchase.ts
│   │       └── ocr.ts               # ⭐ Types para OCR
│   │
│   └── .next/                       # Build output (gitignore)
│
├── launcher/                         # Tauri Desktop App
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── tauri.conf.json              # Configuración Tauri
│   │
│   ├── src/                         # Frontend (HTML básico)
│   │   ├── index.html
│   │   ├── main.js
│   │   └── styles.css
│   │
│   ├── src-tauri/                   # Rust backend
│   │   ├── Cargo.toml
│   │   ├── build.rs
│   │   ├── tauri.conf.json
│   │   │
│   │   ├── src/
│   │   │   ├── main.rs              # Entry point
│   │   │   ├── commands.rs          # Tauri commands
│   │   │   └── utils.rs
│   │   │
│   │   └── icons/                   # App icons
│   │       ├── icon.icns            # Mac
│   │       ├── icon.ico             # Windows
│   │       └── icon.png
│   │
│   └── dist/                        # Build resources
│       ├── backend/                 # Backend compilado
│       ├── frontend/                # Frontend compilado
│       └── database/                # SQLite inicial
│
├── scripts/                         # Build scripts
│   ├── build-backend.sh
│   ├── build-frontend.sh
│   ├── build-launcher.sh
│   ├── build-all.sh                 # Build completo
│   ├── dev-backend.sh               # Dev backend
│   ├── dev-frontend.sh              # Dev frontend
│   └── setup-dev.sh                 # Setup inicial
│
└── installers/                      # Output instaladores
    ├── windows/
    │   └── StockControl-Setup.msi
    └── mac/
        └── StockControl.dmg
```

***

## 📄 ARCHIVOS DE CONFIGURACIÓN BASE

### 1. `backend/requirements.txt`

```txt
# Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1

# Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Validation
pydantic==2.5.3
pydantic-settings==2.1.0

# OCR
pytesseract==0.3.10
opencv-python==4.9.0.80
Pillow==10.2.0

# PDF/Excel
reportlab==4.0.9
openpyxl==3.1.2

# Utils
python-dateutil==2.8.2
```

### 2. `backend/requirements-dev.txt`

```txt
-r requirements.txt

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0

# Code quality
black==24.1.1
flake8==7.0.0
mypy==1.8.0

# PyInstaller
pyinstaller==6.3.0
```

### 3. `backend/main.py`

```python
"""
StockControl Backend API
Entry point de la aplicación FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.v1 import (
    auth,
    users,
    categories,
    products,
    suppliers,
    purchases,
    sales,
    returns,
    cash,
    reports,
    config,
)
from core.config import settings
from db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events
    """
    # Startup: inicializar base de datos
    print("🚀 Inicializando base de datos...")
    init_db()
    print("✅ Base de datos lista")
    
    yield
    
    # Shutdown
    print("👋 Cerrando aplicación...")


app = FastAPI(
    title="StockControl API",
    description="Sistema de gestión de inventario para comercios",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Usuarios"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categorías"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Productos"])
app.include_router(suppliers.router, prefix="/api/v1/suppliers", tags=["Proveedores"])
app.include_router(purchases.router, prefix="/api/v1/purchases", tags=["Compras"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["Ventas"])
app.include_router(returns.router, prefix="/api/v1/returns", tags=["Devoluciones"])
app.include_router(cash.router, prefix="/api/v1/cash", tags=["Caja"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reportes"])
app.include_router(config.router, prefix="/api/v1/config", tags=["Configuración"])


@app.get("/")
def root():
    return {
        "message": "StockControl API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Solo para desarrollo
    )
```

### 4. `backend/core/config.py`

```python
"""
Configuración global usando Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # App
    APP_NAME: str = "StockControl"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_PATH: str = "data/stockcontrol.db"
    DATABASE_URL: str = f"sqlite:///{DATABASE_PATH}"
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    BACKUPS_DIR: Path = DATA_DIR / "backups"
    RECEIPTS_DIR: Path = DATA_DIR / "receipts"
    EXPORTS_DIR: Path = DATA_DIR / "exports"
    
    # OCR
    TESSERACT_CMD: str = None  # None = usar default del sistema
    OCR_LANGUAGE: str = "spa"  # Español
    
    # Business
    DEFAULT_MIN_STOCK: int = 10
    EXPIRY_ALERT_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Crear directorios si no existen
settings.DATA_DIR.mkdir(exist_ok=True)
settings.BACKUPS_DIR.mkdir(exist_ok=True)
settings.RECEIPTS_DIR.mkdir(exist_ok=True)
settings.EXPORTS_DIR.mkdir(exist_ok=True)
```

### 5. `backend/db/base.py`

```python
"""
Base para modelos SQLAlchemy
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

### 6. `backend/db/session.py`

```python
"""
Sesión de base de datos SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Crear engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
)

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency para FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 7. `backend/db/init_db.py`

```python
"""
Inicializar base de datos con datos por defecto
"""

from sqlalchemy.orm import Session

from db.base import Base
from db.session import engine, SessionLocal
from models.user import User
from models.category import Category
from core.security import get_password_hash


def init_db() -> None:
    """
    Crear tablas y datos iniciales
    """
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear datos por defecto
    db = SessionLocal()
    try:
        # Usuario admin por defecto
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                full_name="Administrador",
                role="admin",
                is_active=True,
            )
            db.add(admin)
            print("✅ Usuario admin creado (user: admin, pass: admin123)")
        
        # Categorías por defecto
        default_categories = [
            "Bebidas",
            "Almacén",
            "Limpieza",
            "Snacks",
            "Cigarrillos",
            "Golosinas",
        ]
        
        for cat_name in default_categories:
            cat = db.query(Category).filter(Category.name == cat_name).first()
            if not cat:
                cat = Category(name=cat_name)
                db.add(cat)
        
        db.commit()
        print("✅ Categorías por defecto creadas")
        
    except Exception as e:
        print(f"❌ Error inicializando DB: {e}")
        db.rollback()
    finally:
        db.close()
```

### 8. `frontend/package.json`

```json
{
  "name": "stockcontrol-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "^18",
    "react-dom": "^18",
    "typescript": "^5",
    "@tanstack/react-query": "^5.17.19",
    "zustand": "^4.4.7",
    "react-hook-form": "^7.49.3",
    "zod": "^3.22.4",
    "@hookform/resolvers": "^3.3.4",
    "axios": "^1.6.5",
    "date-fns": "^3.2.0",
    "recharts": "^2.10.3",
    "lucide-react": "^0.303.0",
    "sonner": "^1.3.1",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-tabs": "^1.0.4",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "tailwindcss-animate": "^1.0.7"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "postcss": "^8",
    "tailwindcss": "^3.4.0",
    "eslint": "^8",
    "eslint-config-next": "14.1.0"
  }
}
```

### 9. `frontend/next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',  // Para Tauri/empaquetado
  
  // Variables de entorno
  env: {
    API_URL: process.env.API_URL || 'http://localhost:8000',
  },
  
  // Optimizaciones
  compress: true,
  poweredByHeader: false,
  
  // Experimental
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
}

module.exports = nextConfig
```

### 10. `frontend/tailwind.config.ts`

```typescript
import type { Config } from "tailwindcss"

const config = {
  darkMode: ["class"],
  content: [
    './src/pages/**/*.{ts,tsx}',
    './src/components/**/*.{ts,tsx}',
    './src/app/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        // StockControl palette
        primary: {
          DEFAULT: "#2196F3",
          50: "#E3F2FD",
          100: "#BBDEFB",
          500: "#2196F3",
          600: "#1E88E5",
          700: "#1976D2",
        },
        success: {
          DEFAULT: "#4CAF50",
          50: "#E8F5E9",
          500: "#4CAF50",
        },
        danger: {
          DEFAULT: "#F44336",
          50: "#FFEBEE",
          500: "#F44336",
        },
        warning: {
          DEFAULT: "#FF9800",
          50: "#FFF3E0",
          500: "#FF9800",
        },
        purple: {
          500: "#9C27B0",
          50: "#F3E5F5",
        },
        indigo: {
          500: "#3F51B5",
          50: "#E8EAF6",
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config

export default config
```

### 11. `frontend/src/lib/api.ts`

```typescript
/**
 * API client usando axios
 */

import axios from 'axios';

const API_URL = process.env.API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado, redirect a login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### 12. `scripts/setup-dev.sh`

```bash
#!/bin/bash

echo "🚀 Setup StockControl - Desarrollo"
echo ""

# Backend
echo "📦 Instalando dependencias backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cd ..

# Frontend
echo "🎨 Instalando dependencias frontend..."
cd frontend
pnpm install
cd ..

# Launcher
echo "🖥️  Instalando dependencias launcher..."
cd launcher
pnpm install
cd ..

echo ""
echo "✅ Setup completado!"
echo ""
echo "Para iniciar desarrollo:"
echo "  Backend:  cd backend && source venv/bin/activate && python main.py"
echo "  Frontend: cd frontend && pnpm dev"
```

### 13. `.gitignore` (raíz)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env

# Node
node_modules/
.next/
.pnpm-store/

# Build
dist/
build/
*.egg-info/

# Data
backend/data/*.db
backend/data/backups/
backend/data/receipts/
backend/data/exports/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Installers
installers/
```

***

## 🚀 COMANDOS PARA CREAR LA ESTRUCTURA

```bash
# Crear proyecto base
mkdir StockControl
cd StockControl

# Crear estructura de carpetas backend
mkdir -p backend/{api/v1,core,db/migrations,models,schemas,services,utils,data/{backups,receipts,exports}}

# Crear estructura frontend
mkdir -p frontend/src/{app/{(auth)/login,(dashboard)/{ventas,devoluciones,stock,productos,compras/ocr,proveedores,caja/cierre,reportes,configuracion}},components/{ui,layout,ventas,productos,compras,stock,caja,reportes,shared},hooks,lib,store,types}

# Crear estructura launcher
mkdir -p launcher/{src,src-tauri/{src,icons},dist/{backend,frontend,database}}

# Crear carpetas adicionales
mkdir -p {docs,scripts,installers/{windows,mac}}

# Crear archivos base
touch README.md .gitignore docker-compose.yml
touch backend/{main.py,config.py,requirements.txt,requirements-dev.txt,build.spec,.env.example}
touch frontend/{package.json,next.config.js,tailwind.config.ts,tsconfig.json,.env.local.example}
touch scripts/{setup-dev.sh,build-all.sh,dev-backend.sh,dev-frontend.sh}
```

***

## ✅ CHECKLIST PASO 1 COMPLETADO

- ✅ Estructura de carpetas completa
- ✅ Archivos de configuración base
- ✅ package.json con dependencias
- ✅ Scripts de desarrollo
- ✅ Gitignore configurado

**Próximo paso:** ¿Querés que te arme el **PASO 2 (Base de datos completa con modelos SQLAlchemy)?**