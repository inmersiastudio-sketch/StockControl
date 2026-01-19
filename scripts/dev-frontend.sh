#!/bin/bash
# Iniciar frontend en modo desarrollo

cd "$(dirname "$0")/../frontend"

if [ ! -d "node_modules" ]; then
    echo "❌ node_modules no encontrado. Ejecutá primero: ./scripts/setup-dev.sh"
    exit 1
fi

echo "🎨 Iniciando frontend en http://localhost:3000"
echo ""
npm run dev
