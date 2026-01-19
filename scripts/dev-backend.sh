#!/bin/bash
# Iniciar backend en modo desarrollo

cd "$(dirname "$0")/../backend"

if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecutá primero: ./scripts/setup-dev.sh"
    exit 1
fi

source venv/bin/activate
echo "🚀 Iniciando backend en http://localhost:8000"
echo "📚 Documentación: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --port 8000
