"""
Endpoints de Autenticación
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.config import settings
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserResponse, UserCreate

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login con username y password
    Retorna JWT token
    """
    # Buscar usuario
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar password
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Obtener información del usuario actual
    """
    return current_user


@router.post("/register-admin", response_model=UserResponse)
def register_first_admin(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar el primer usuario administrador.
    Solo funciona si no hay ningún usuario en el sistema.
    """
    # Verificar si ya existen usuarios
    existing_users = db.query(User).count()
    if existing_users > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ya existe un administrador. Use el login normal."
        )
    
    # Crear usuario admin
    new_user = User(
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role="admin",
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
