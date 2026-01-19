"""
Configuración de la aplicación
Todas las variables de configuración centralizadas
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings"""
    
    # Aplicación
    APP_NAME: str = "StockControl"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Base de datos
    DATABASE_URL: str = "sqlite:///./stockcontrol.db"
    
    # Seguridad
    SECRET_KEY: str = "tu-clave-secreta-cambiar-en-produccion-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    
    # CORS - Orígenes permitidos
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js dev
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]
    
    # OCR
    TESSERACT_CMD: str = ""  # Se configura según el OS
    
    # Rutas de archivos
    UPLOAD_DIR: str = "uploads"
    RECEIPTS_DIR: str = "uploads/receipts"
    BACKUPS_DIR: str = "backups"
    
    # Configuración de negocio (defaults)
    DEFAULT_MIN_STOCK: int = 10
    EXPIRATION_ALERT_DAYS: int = 7
    ALLOW_ZERO_STOCK_SALES: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()

# Crear directorios necesarios
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RECEIPTS_DIR, exist_ok=True)
os.makedirs(settings.BACKUPS_DIR, exist_ok=True)
