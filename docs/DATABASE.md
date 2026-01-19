# StockControl - Schema de Base de Datos

## Diagrama de Relaciones

```
users
  │
  ├── sales (user_id)
  │     └── sale_items (sale_id)
  │           └── products (product_id)
  │
  ├── purchases (user_id)
  │     ├── purchase_items (purchase_id)
  │     │     └── products (product_id)
  │     └── suppliers (supplier_id)
  │
  ├── cash_movements (user_id)
  │
  └── cash_closures (user_id)

products
  ├── categories (category_id)
  └── product_lots (product_id)
        └── purchases (purchase_id)
```

## Tablas

### users
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| username | VARCHAR(50) UNIQUE | Usuario de login |
| password_hash | VARCHAR(255) | Contraseña hasheada |
| full_name | VARCHAR(100) | Nombre completo |
| role | VARCHAR(20) | 'admin' o 'employee' |
| is_active | BOOLEAN | Estado activo |
| created_at | TIMESTAMP | Fecha creación |

### categories
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| name | VARCHAR(100) UNIQUE | Nombre categoría |
| description | VARCHAR(255) | Descripción |
| created_at | TIMESTAMP | Fecha creación |

### suppliers
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| name | VARCHAR(200) | Nombre proveedor |
| cuit | VARCHAR(20) | CUIT (XX-XXXXXXXX-X) |
| phone | VARCHAR(50) | Teléfono |
| email | VARCHAR(100) | Email |
| address | TEXT | Dirección |
| is_active | BOOLEAN | Estado activo |
| created_at | TIMESTAMP | Fecha creación |

### products
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| code | VARCHAR(50) UNIQUE | Código interno |
| barcode | VARCHAR(50) | Código de barras |
| name | VARCHAR(200) | Nombre producto |
| description | TEXT | Descripción |
| category_id | INTEGER FK | Categoría |
| cost | FLOAT | Costo promedio |
| price | FLOAT | Precio de venta |
| min_stock | INTEGER | Stock mínimo alerta |
| is_active | BOOLEAN | Estado activo |
| created_at | TIMESTAMP | Fecha creación |

### product_lots (FIFO)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| product_id | INTEGER FK | Producto |
| quantity | INTEGER | Cantidad actual |
| initial_quantity | INTEGER | Cantidad inicial |
| cost | FLOAT | Costo del lote |
| expiration_date | DATE | Fecha vencimiento |
| purchase_id | INTEGER FK | Compra origen |
| created_at | TIMESTAMP | Fecha creación |

### sales
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| subtotal | FLOAT | Subtotal |
| discount | FLOAT | Descuento |
| total | FLOAT | Total |
| payment_method | VARCHAR(20) | cash/card/transfer |
| amount_paid | FLOAT | Monto pagado |
| change_given | FLOAT | Vuelto |
| user_id | INTEGER FK | Vendedor |
| is_cancelled | BOOLEAN | Anulada |
| cancelled_by_id | INTEGER FK | Quién anuló |
| cancel_reason | TEXT | Motivo anulación |
| created_at | TIMESTAMP | Fecha venta |

### sale_items
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| sale_id | INTEGER FK | Venta |
| product_id | INTEGER FK | Producto |
| quantity | INTEGER | Cantidad |
| unit_price | FLOAT | Precio unitario |
| unit_cost | FLOAT | Costo unitario |
| subtotal | FLOAT | Subtotal |

### purchases
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| supplier_id | INTEGER FK | Proveedor |
| total | FLOAT | Total compra |
| notes | TEXT | Notas |
| receipt_image_path | VARCHAR(500) | Ruta imagen ticket |
| ocr_raw_text | TEXT | Texto OCR |
| ocr_data | JSON | Datos estructurados OCR |
| user_id | INTEGER FK | Quién registró |
| purchase_date | DATE | Fecha del ticket |
| created_at | TIMESTAMP | Fecha registro |

### purchase_items
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| purchase_id | INTEGER FK | Compra |
| product_id | INTEGER FK | Producto |
| quantity | INTEGER | Cantidad |
| unit_cost | FLOAT | Costo unitario |
| subtotal | FLOAT | Subtotal |
| expiration_date | DATE | Vencimiento |

### cash_movements
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| type | VARCHAR(20) | income/expense |
| amount | FLOAT | Monto |
| method | VARCHAR(20) | cash/card/transfer |
| description | TEXT | Descripción |
| user_id | INTEGER FK | Usuario |
| created_at | TIMESTAMP | Fecha |

### cash_closures
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PK | ID único |
| date | DATE UNIQUE | Fecha cierre |
| expected_cash | FLOAT | Esperado sistema |
| counted_cash | FLOAT | Contado físico |
| difference | FLOAT | Diferencia |
| bills_count | JSON | Detalle billetes |
| total_sales_cash | FLOAT | Ventas efectivo |
| total_sales_card | FLOAT | Ventas tarjeta |
| total_sales_transfer | FLOAT | Ventas transfer |
| total_incomes | FLOAT | Ingresos extra |
| total_expenses | FLOAT | Egresos |
| notes | TEXT | Observaciones |
| user_id | INTEGER FK | Quién cerró |
| created_at | TIMESTAMP | Fecha registro |
