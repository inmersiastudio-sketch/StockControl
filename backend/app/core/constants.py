"""
Constantes globales de la aplicación
"""

# Roles de usuario
ROLE_ADMIN = "admin"
ROLE_EMPLOYEE = "employee"
ROLES = [ROLE_ADMIN, ROLE_EMPLOYEE]

# Métodos de pago
PAYMENT_CASH = "cash"
PAYMENT_CARD = "card"
PAYMENT_TRANSFER = "transfer"
PAYMENT_METHODS = [PAYMENT_CASH, PAYMENT_CARD, PAYMENT_TRANSFER]

# Tipos de movimiento de caja
MOVEMENT_INCOME = "income"
MOVEMENT_EXPENSE = "expense"
MOVEMENT_TYPES = [MOVEMENT_INCOME, MOVEMENT_EXPENSE]

# Denominaciones de billetes argentinos (para arqueo)
BILL_DENOMINATIONS = [
    {"value": 10000, "label": "$10.000"},
    {"value": 5000, "label": "$5.000"},
    {"value": 2000, "label": "$2.000"},
    {"value": 1000, "label": "$1.000"},
    {"value": 500, "label": "$500"},
    {"value": 200, "label": "$200"},
    {"value": 100, "label": "$100"},
    {"value": 50, "label": "$50"},
    {"value": 20, "label": "$20"},
    {"value": 10, "label": "$10"},
]

# Categorías por defecto
DEFAULT_CATEGORIES = [
    "Bebidas",
    "Almacén",
    "Limpieza",
    "Snacks",
    "Cigarrillos",
    "Golosinas",
    "Lácteos",
    "Fiambres",
    "Panificados",
    "Otros",
]

# Mensajes de error comunes
ERROR_NOT_FOUND = "Recurso no encontrado"
ERROR_UNAUTHORIZED = "No autorizado"
ERROR_FORBIDDEN = "Acceso denegado"
ERROR_INVALID_CREDENTIALS = "Credenciales inválidas"
ERROR_DUPLICATE = "Ya existe un registro con estos datos"
