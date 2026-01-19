"""
Configuración de sesión de base de datos
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Crear engine de SQLite
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG
)

# Sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
