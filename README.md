# StockControl - Sistema de Inventario para Despensas

Sistema de gestión de inventario local para despensas y almacenes argentinos.
Incluye ventas, stock con FIFO, caja, reportes y OCR para carga automática de tickets.

## 🏗️ Estructura del Proyecto

```
Proyect-Despensa/
├── backend/                 # API con FastAPI + SQLite
│   ├── app/
│   │   ├── main.py         # Punto de entrada
│   │   ├── core/           # Config, DB, seguridad
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── api/            # Endpoints REST
│   │   └── services/       # Lógica de negocio
│   ├── requirements.txt
│   └── README.md
├── frontend/               # UI con Next.js 14 + Tailwind
│   ├── src/
│   │   ├── app/           # App Router
│   │   ├── components/    # Componentes React
│   │   ├── lib/           # API client, utils
│   │   └── store/         # Estado con Zustand
│   ├── package.json
│   └── README.md
└── docs/                   # Documentación
```

## 🚀 Inicio Rápido

### Requisitos
- Python 3.11+
- Node.js 18+
- Git

### 1. Clonar e instalar Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Instalar Frontend

```bash
cd frontend
npm install
```

### 3. Ejecutar en desarrollo

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Acceder a la aplicación

- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **API ReDoc:** http://localhost:8000/redoc

## 📋 Primer Uso

1. Ir a http://localhost:8000/docs
2. Usar `POST /api/v1/auth/register-admin` para crear el primer admin
3. Ir a http://localhost:3000 y hacer login

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web async
- **SQLAlchemy** - ORM
- **SQLite** - Base de datos local
- **Pydantic** - Validación de datos
- **JWT** - Autenticación

### Frontend
- **Next.js 14** - Framework React con App Router
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos
- **Zustand** - Estado global
- **TanStack Query** - Fetching de datos
- **React Hook Form + Zod** - Formularios

## 📊 Roadmap

- [x] Sprint 1: Estructura base + Auth + Productos
- [ ] Sprint 2: Ventas
- [ ] Sprint 3: FIFO + Ganancias
- [ ] Sprint 4: Compras manual
- [ ] Sprint 5: OCR de tickets
- [ ] Sprint 6: Caja + Reportes
- [ ] Sprint 7: Devoluciones + Config
- [ ] Sprint 8: Packaging desktop

## 📄 Licencia

Proyecto privado - Todos los derechos reservados.
