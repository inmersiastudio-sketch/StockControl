"""
Endpoints de Gestión de Usuarios (Solo Admin)
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import DBSession, CurrentAdmin
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def list_users(
    db: DBSession,
    current_user: CurrentAdmin,
    skip: int = 0,
    limit: int = 100,
):
    """
    Listar todos los usuarios
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Crear nuevo usuario (empleado o admin)
    """
    # Verificar que el username no exista
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe",
        )
    
    # Validar role
    role_value = user_in.role.value if hasattr(user_in.role, 'value') else user_in.role
    if role_value not in ["admin", "employee"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol inválido. Debe ser 'admin' o 'employee'",
        )
    
    # Crear usuario
    user = User(
        username=user_in.username,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=role_value,
        is_active=True,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Obtener un usuario por ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Actualizar usuario
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    # No permitir que el admin se desactive a sí mismo
    if user.id == current_user.id and user_in.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivarte a ti mismo"
        )
    
    # Actualizar campos
    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    
    if user_in.password is not None:
        user.password_hash = get_password_hash(user_in.password)
    
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Eliminar usuario (solo si no tiene ventas)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    # No permitir eliminar si tiene ventas
    if user.sales:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un usuario con ventas registradas. Desactívalo en su lugar.",
        )
    
    # No permitir eliminarse a sí mismo
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propio usuario",
        )
    
    db.delete(user)
    db.commit()
    
    return None
