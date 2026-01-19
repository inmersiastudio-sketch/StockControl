# StockControl - Product Requirements Document

## 1. Visión del Producto

### ¿Qué es?
Sistema de gestión de inventario local (desktop) para despensas y almacenes argentinos que automatiza ventas, stock, caja y reportes con interfaz simple y OCR para carga automática de stock desde tickets de compra.

### ¿Para quién?
- Dueños de despensas/almacenes pequeños (5-50m²)
- Sin conocimientos técnicos avanzados
- Con o sin internet en el local
- 1-5 empleados

### Propuesta de valor única
"El único sistema que carga el stock automáticamente sacándole foto al ticket de compra de tu distribuidora. Funciona sin internet, instalación en el día."

## 2. Roles de Usuario

### EMPLEADO (Cajero)
- Realizar ventas
- Procesar devoluciones (con aprobación admin)
- Consultar stock
- Ver su historial de ventas del día

### ADMIN (Dueño/Encargado)
- Todo lo que hace el empleado
- Gestionar productos (CRUD)
- Registrar compras (manual y OCR)
- Gestionar proveedores
- Movimientos de caja
- Cierre de caja diario
- Reportes completos
- Gestión de empleados
- Configuración del sistema

## 3. Funcionalidades Core

Ver DocumentacionInicial.md para el detalle completo de cada funcionalidad.

## 4. Stack Tecnológico

### Backend
- FastAPI + SQLite + SQLAlchemy
- JWT para autenticación
- Tesseract OCR

### Frontend
- Next.js 14 + TypeScript
- Tailwind CSS
- Zustand + TanStack Query

### Desktop (futuro)
- Tauri

## 5. Roadmap

1. Sprint 1: Base + Auth + Productos
2. Sprint 2: Ventas
3. Sprint 3: FIFO + Ganancias
4. Sprint 4: Compras manual
5. Sprint 5: OCR
6. Sprint 6: Caja + Reportes
7. Sprint 7: Devoluciones + Config
8. Sprint 8: Packaging desktop
