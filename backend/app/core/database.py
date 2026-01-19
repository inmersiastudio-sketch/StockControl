"""
Configuración de la base de datos SQLite con SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Crear engine de SQLite
# check_same_thread=False es necesario para SQLite con FastAPI
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG  # Muestra queries SQL en modo debug
)

# Sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def create_tables():
    """Crear todas las tablas definidas en los modelos"""
    # Importar modelos para que SQLAlchemy los registre
    from app.models import user, category, supplier, product, sale, purchase, cash
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency para obtener sesión de base de datos.
    Se usa en los endpoints con Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
