#!/bin/bash
# Setup inicial para desarrollo

echo "🚀 Setup StockControl - Desarrollo"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instalá Python 3.11+"
    exit 1
fi

# Verificar Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no encontrado. Instalá Node.js 18+"
    exit 1
fi

# Backend
echo "📦 Configurando backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Entorno virtual creado"
fi

source venv/bin/activate
pip install -r requirements.txt --quiet
echo "   ✅ Dependencias instaladas"

# Crear .env si no existe
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "   ✅ Archivo .env creado"
fi

cd ..

# Frontend
echo ""
echo "🎨 Configurando frontend..."
cd frontend
npm install --silent
echo "   ✅ Dependencias instaladas"

# Crear .env.local si no existe
if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
    echo "   ✅ Archivo .env.local creado"
fi

cd ..

echo ""
echo "✅ ¡Setup completado!"
echo ""
echo "Para iniciar desarrollo:"
echo ""
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    uvicorn app.main:app --reload --port 8000"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "Luego abrí http://localhost:3000"
