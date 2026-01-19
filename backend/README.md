# StockControl Backend
# Sistema de Inventario para Despensas y Almacenes

## Requisitos

- Python 3.11+
- pip

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar servidor de desarrollo:
```bash
uvicorn app.main:app --reload --port 8000
```

4. Acceder a la documentación:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py           # Punto de entrada de FastAPI
│   ├── core/             # Configuración, seguridad, base de datos
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Schemas Pydantic
│   ├── api/              # Endpoints de la API
│   └── services/         # Lógica de negocio
├── tests/                # Tests
├── uploads/              # Archivos subidos (tickets)
├── backups/              # Backups de la base de datos
├── requirements.txt      # Dependencias
└── .env                  # Variables de entorno (crear manualmente)
```

## Primer uso

1. Ejecutar el servidor
2. Ir a http://localhost:8000/docs
3. Usar el endpoint POST `/api/v1/auth/register-admin` para crear el primer usuario administrador
4. Usar el endpoint POST `/api/v1/auth/login` para obtener el token JWT
