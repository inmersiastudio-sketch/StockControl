"""
Inicializar base de datos con datos por defecto y de prueba
"""

from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models import (
    User,
    Category,
    Supplier,
    Product,
    ProductLot,
)
from app.core.security import get_password_hash


def create_default_users(db: Session):
    """Crear usuarios por defecto"""
    # Admin
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            full_name="Administrador",
            role="admin",
            is_active=True,
        )
        db.add(admin)
        print("✅ Usuario admin creado (user: admin, pass: admin123)")

    # Empleado de prueba
    employee = db.query(User).filter(User.username == "cajero").first()
    if not employee:
        employee = User(
            username="cajero",
            password_hash=get_password_hash("cajero123"),
            full_name="María González (Cajera)",
            role="employee",
            is_active=True,
        )
        db.add(employee)
        print("✅ Usuario cajero creado (user: cajero, pass: cajero123)")


def create_default_categories(db: Session):
    """Crear categorías por defecto"""
    default_categories = [
        "Bebidas",
        "Almacén",
        "Limpieza",
        "Snacks",
        "Cigarrillos",
        "Golosinas",
        "Lácteos",
        "Panadería",
    ]

    for cat_name in default_categories:
        cat = db.query(Category).filter(Category.name == cat_name).first()
        if not cat:
            cat = Category(name=cat_name)
            db.add(cat)

    print(f"✅ {len(default_categories)} categorías creadas")


def create_sample_suppliers(db: Session):
    """Crear proveedores de ejemplo"""
    suppliers_data = [
        {
            "name": "Distribuidora San Martín",
            "cuit": "30-12345678-9",
            "phone": "0351-4567890",
            "email": "ventas@sanmartin.com.ar",
        },
        {
            "name": "Mayorista El Sol",
            "cuit": "30-98765432-1",
            "phone": "0351-1234567",
        },
    ]

    for supplier_data in suppliers_data:
        supplier = db.query(Supplier).filter(
            Supplier.name == supplier_data["name"]
        ).first()
        if not supplier:
            supplier = Supplier(**supplier_data)
            db.add(supplier)

    print("✅ Proveedores de ejemplo creados")


def create_sample_products(db: Session):
    """Crear productos de ejemplo con stock"""
    # Obtener categorías
    bebidas = db.query(Category).filter(Category.name == "Bebidas").first()
    almacen = db.query(Category).filter(Category.name == "Almacén").first()
    snacks = db.query(Category).filter(Category.name == "Snacks").first()

    if not all([bebidas, almacen, snacks]):
        print("⚠️  No se encontraron categorías")
        return

    products_data = [
        # Bebidas
        {
            "code": "7790001001",
            "name": "Coca Cola 2.25L",
            "category_id": bebidas.id,
            "cost": 1200.0,
            "price": 2500.0,
            "min_stock": 12,
            "stock": 48,
            "expiration": date.today() + timedelta(days=180),
        },
        {
            "code": "7790001002",
            "name": "Sprite 2.25L",
            "category_id": bebidas.id,
            "cost": 1100.0,
            "price": 2200.0,
            "min_stock": 12,
            "stock": 36,
            "expiration": date.today() + timedelta(days=180),
        },
        {
            "code": "7790001003",
            "name": "Agua Mineral 500ml",
            "category_id": bebidas.id,
            "cost": 300.0,
            "price": 600.0,
            "min_stock": 24,
            "stock": 120,
            "expiration": date.today() + timedelta(days=365),
        },
        # Almacén
        {
            "code": "7790002001",
            "name": "Arroz Gallo Oro 1kg",
            "category_id": almacen.id,
            "cost": 800.0,
            "price": 1500.0,
            "min_stock": 10,
            "stock": 25,
            "expiration": date.today() + timedelta(days=730),
        },
        {
            "code": "7790002002",
            "name": "Fideos Matarazzo 500g",
            "category_id": almacen.id,
            "cost": 600.0,
            "price": 1200.0,
            "min_stock": 15,
            "stock": 40,
            "expiration": date.today() + timedelta(days=365),
        },
        # Snacks
        {
            "code": "7790003001",
            "name": "Galletitas Oreo 118g",
            "category_id": snacks.id,
            "cost": 450.0,
            "price": 950.0,
            "min_stock": 10,
            "stock": 8,  # Stock bajo (alerta)
            "expiration": date.today() + timedelta(days=90),
        },
        {
            "code": "7790003002",
            "name": "Papas Lays 170g",
            "category_id": snacks.id,
            "cost": 800.0,
            "price": 1600.0,
            "min_stock": 12,
            "stock": 20,
            "expiration": date.today() + timedelta(days=60),
        },
        {
            "code": "7790003003",
            "name": "Chocolate Milka 100g",
            "category_id": snacks.id,
            "cost": 1000.0,
            "price": 2000.0,
            "min_stock": 10,
            "stock": 15,
            "expiration": date.today() + timedelta(days=5),  # Próximo a vencer (alerta)
        },
    ]

    for product_data in products_data:
        product = db.query(Product).filter(
            Product.code == product_data["code"]
        ).first()

        if not product:
            # Extraer datos de stock y vencimiento
            stock = product_data.pop("stock")
            expiration = product_data.pop("expiration")

            # Crear producto
            product = Product(**product_data)
            db.add(product)
            db.flush()  # Para obtener el ID

            # Crear lote inicial
            lot = ProductLot(
                product_id=product.id,
                quantity=stock,
                cost=product.cost,
                expiration_date=expiration,
            )
            db.add(lot)

    print("✅ Productos de ejemplo creados con stock")


def init_db() -> None:
    """
    Crear tablas y datos iniciales
    """
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas")

    # Crear datos por defecto
    db = SessionLocal()
    try:
        create_default_users(db)
        create_default_categories(db)
        create_sample_suppliers(db)
        create_sample_products(db)

        db.commit()
        print("\n🎉 Base de datos inicializada correctamente!")
        print("\n📝 Usuarios disponibles:")
        print("   - Admin: user='admin' pass='admin123'")
        print("   - Cajero: user='cajero' pass='cajero123'")

    except Exception as e:
        print(f"❌ Error inicializando DB: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
