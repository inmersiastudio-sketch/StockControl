"""
Endpoints de Categorías
"""

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import DBSession, CurrentAdmin
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """
    Listar todas las categorías (sin autenticación requerida)
    """
    categories = db.query(Category).order_by(Category.name).all()
    return categories


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Crear nueva categoría (solo admin)
    """
    # Verificar que no exista
    existing = db.query(Category).filter(Category.name == category_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría ya existe",
        )
    
    category = Category(
        name=category_in.name,
        description=getattr(category_in, 'description', None)
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return category


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """
    Obtener categoría por ID (sin auth)
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: DBSession,
    current_user: CurrentAdmin,
):
    """
    Eliminar categoría (solo si no tiene productos)
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    
    # Verificar que no tenga productos
    if category.products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. Hay {len(category.products)} productos en esta categoría",
        )
    
    db.delete(category)
    db.commit()
    
    return None
