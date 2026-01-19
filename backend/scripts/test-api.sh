#!/bin/bash

echo "🧪 Testing StockControl API"

API_URL="http://localhost:8000/api/v1"

# 1. Login
echo "1️⃣  Testing Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123")

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
  echo "✅ Login exitoso"
  echo "   Token: ${TOKEN:0:50}..."
else
  echo "❌ Login falló"
  echo "   Response: $LOGIN_RESPONSE"
  exit 1
fi

# 2. Obtener usuario actual
echo ""
echo "2️⃣  Testing Get Current User..."
curl -s -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null || echo "Error parsing JSON"

# 3. Listar categorías (sin auth)
echo ""
echo "3️⃣  Testing List Categories (no auth)..."
curl -s -X GET "$API_URL/categories" | python3 -m json.tool 2>/dev/null || echo "Error parsing JSON"

# 4. Listar productos
echo ""
echo "4️⃣  Testing List Products..."
curl -s -X GET "$API_URL/products" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null || echo "Error parsing JSON"

# 5. Listar proveedores
echo ""
echo "5️⃣  Testing List Suppliers..."
curl -s -X GET "$API_URL/suppliers" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null || echo "Error parsing JSON"

# 6. Estadísticas del día
echo ""
echo "6️⃣  Testing Today Stats..."
curl -s -X GET "$API_URL/sales/stats/today" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null || echo "Error parsing JSON"

# 7. Alertas de stock bajo
echo ""
echo "7️⃣  Testing Low Stock Alerts..."
curl -s -X GET "$API_URL/products/alerts/low-stock" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null || echo "Error parsing JSON"

# 8. Productos próximos a vencer
echo ""
echo "8️⃣  Testing Expiring Soon..."
curl -s -X GET "$API_URL/products/alerts/expiring-soon?days=30" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null || echo "Error parsing JSON"

echo ""
echo "✅ Tests completados"
echo ""
echo "📝 Para probar la creación de ventas, usa:"
echo "   curl -X POST '$API_URL/sales' \\"
echo "     -H 'Authorization: Bearer $TOKEN' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"items\": [{\"product_id\": 1, \"quantity\": 2}], \"payment_method\": \"cash\", \"discount\": 0}'"
