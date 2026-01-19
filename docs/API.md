# StockControl - Documentación de API

Base URL: `http://localhost:8000/api/v1`

## Autenticación

Todos los endpoints (excepto login) requieren token JWT en el header:
```
Authorization: Bearer <token>
```

### POST /auth/login
Login de usuario.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "full_name": "Administrador",
    "role": "admin",
    "is_active": true
  }
}
```

### POST /auth/register-admin
Registrar primer admin (solo si no hay usuarios).

### GET /auth/me
Obtener usuario actual.

---

## Productos

### GET /products
Listar productos.

**Query params:**
- `search`: Buscar por nombre/código
- `category_id`: Filtrar por categoría
- `low_stock`: Solo stock bajo
- `active_only`: Solo activos (default: true)

### POST /products
Crear producto (Admin).

### GET /products/{id}
Obtener producto con lotes.

### PATCH /products/{id}
Actualizar producto (Admin).

### DELETE /products/{id}
Desactivar producto (Admin).

---

## Categorías

### GET /categories
### POST /categories (Admin)
### PATCH /categories/{id} (Admin)
### DELETE /categories/{id} (Admin)

---

## Proveedores

### GET /suppliers (Admin)
### POST /suppliers (Admin)
### PATCH /suppliers/{id} (Admin)
### DELETE /suppliers/{id} (Admin)

---

## Ventas (Sprint 2)

### GET /sales
### POST /sales
### POST /sales/{id}/cancel

---

## Compras (Sprint 4-5)

### GET /purchases (Admin)
### POST /purchases (Admin)
### POST /purchases/ocr (Admin)

---

## Caja (Sprint 6)

### GET /cash/summary (Admin)
### POST /cash/movement (Admin)
### POST /cash/close (Admin)

---

## Reportes (Sprint 6)

### GET /reports/daily (Admin)
### GET /reports/period (Admin)
### GET /reports/alerts (Admin)
