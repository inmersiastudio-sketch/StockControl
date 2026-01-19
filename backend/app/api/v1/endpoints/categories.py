"""
Endpoints de Categorías
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
async def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listar todas las categorías
    """
    categories = db.query(Category).all()
    
    result = []
    for cat in categories:
        cat_dict = CategoryResponse.model_validate(cat)
        cat_dict.product_count = db.query(Product).filter(Product.category_id == cat.id).count()
        result.append(cat_dict)
    
    return result


@router.post("/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Crear una categoría (Solo Admin)
    """
    # Verificar si ya existe
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La categoría '{category_data.name}' ya existe"
        )
    
    new_category = Category(
        name=category_data.name,
        description=category_data.description
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    response = CategoryResponse.model_validate(new_category)
    response.product_count = 0
    return response


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener una categoría por ID
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    response = CategoryResponse.model_validate(category)
    response.product_count = db.query(Product).filter(Product.category_id == category.id).count()
    return response


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Actualizar una categoría (Solo Admin)
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Verificar nombre duplicado
    if category_data.name:
        existing = db.query(Category).filter(
            Category.name == category_data.name,
            Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe otra categoría con el nombre '{category_data.name}'"
            )
    
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    response = CategoryResponse.model_validate(category)
    response.product_count = db.query(Product).filter(Product.category_id == category.id).count()
    return response


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Eliminar una categoría (Solo Admin)
    Solo si no tiene productos asociados.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Verificar si tiene productos
    product_count = db.query(Product).filter(Product.category_id == category_id).count()
    if product_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. Tiene {product_count} productos asociados."
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": f"Categoría '{category.name}' eliminada"}
