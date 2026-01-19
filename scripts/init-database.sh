#!/bin/bash

echo "🗄️  Inicializando base de datos StockControl..."

# Ir al directorio del proyecto
cd "$(dirname "$0")/.."

# Activar entorno virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "backend/venv" ]; then
    source backend/venv/bin/activate
fi

# Ejecutar inicialización
cd backend
python -c "from app.db.init_db import init_db; init_db()"

echo ""
echo "✅ Base de datos lista!"
echo ""
echo "Para verificar, ejecuta:"
echo "  sqlite3 backend/data/stockcontrol.db '.tables'"
