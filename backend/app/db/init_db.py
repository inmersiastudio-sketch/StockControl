"""
Inicializar base de datos con datos por defecto
"""

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.core.security import get_password_hash
from app.core.constants import DEFAULT_CATEGORIES
from app.models.user import User
from app.models.category import Category


def init_db() -> None:
    """
    Crear tablas y datos iniciales
    """
    # Importar todos los modelos para que se registren
    from app.models import user, category, supplier, product, sale, purchase, cash
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar si ya hay datos
        existing_users = db.query(User).count()
        
        if existing_users == 0:
            # Crear usuario admin por defecto
            admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                full_name="Administrador",
                role="admin",
                is_active=True,
            )
            db.add(admin)
            print("✅ Usuario admin creado (user: admin, pass: admin123)")
        
        # Crear categorías por defecto si no existen
        existing_categories = db.query(Category).count()
        if existing_categories == 0:
            for cat_name in DEFAULT_CATEGORIES:
                category = Category(name=cat_name)
                db.add(category)
            print(f"✅ {len(DEFAULT_CATEGORIES)} categorías creadas")
        
        db.commit()
        
    except Exception as e:
        print(f"❌ Error inicializando DB: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Inicializando base de datos...")
    init_db()
    print("¡Listo!")
