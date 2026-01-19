"""
Dependencias para FastAPI (Auth, DB)
"""

from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenData

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    Obtener usuario actual desde JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username, role=payload.get("role"))
    
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Validar que el usuario actual sea admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador",
        )
    return current_user


# Type aliases para usar en endpoints
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAdmin = Annotated[User, Depends(get_current_admin)]
DBSession = Annotated[Session, Depends(get_db)]


# Re-exportar para uso fácil en endpoints
__all__ = [
    "get_db",
    "get_current_user", 
    "get_current_admin",
    "CurrentUser",
    "CurrentAdmin",
    "DBSession",
    "Session",
    "User",
]
