"""
Schemas de Usuario para validación de datos
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    employee = "employee"


# --- Schemas de entrada ---

class UserCreate(BaseModel):
    """Schema para crear un usuario"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = UserRole.employee


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserPasswordChange(BaseModel):
    """Schema para cambiar contraseña"""
    current_password: str
    new_password: str = Field(..., min_length=4)


# --- Schemas de salida ---

class UserResponse(BaseModel):
    """Schema de respuesta para usuario (sin password)"""
    id: int
    username: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserWithStats(UserResponse):
    """Usuario con estadísticas de ventas"""
    total_sales: int = 0
    total_amount: float = 0


# --- Schemas de autenticación ---

class Token(BaseModel):
    """Schema de respuesta del login"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LoginRequest(BaseModel):
    """Schema de petición de login"""
    username: str
    password: str
