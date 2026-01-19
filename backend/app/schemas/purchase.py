"""
Schemas de Compra y OCR
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


# --- Items de compra ---

class PurchaseItemCreate(BaseModel):
    """Item para agregar a una compra"""
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_cost: float = Field(..., gt=0)
    expiration_date: Optional[date] = None


class PurchaseItemResponse(BaseModel):
    """Respuesta de item de compra"""
    id: int
    product_id: int
    product_name: str = ""
    product_code: str = ""
    quantity: int
    unit_cost: float
    subtotal: float
    expiration_date: Optional[date]
    
    class Config:
        from_attributes = True


# --- Compra completa ---

class PurchaseCreate(BaseModel):
    """Schema para crear una compra manual"""
    supplier_id: Optional[int] = None
    items: List[PurchaseItemCreate] = Field(..., min_length=1)
    notes: Optional[str] = None
    purchase_date: Optional[date] = None


class PurchaseResponse(BaseModel):
    """Schema de respuesta para compra"""
    id: int
    supplier_id: Optional[int]
    supplier_name: Optional[str] = None
    total: float
    notes: Optional[str]
    receipt_image_path: Optional[str]
    user_id: int
    user_name: str = ""
    purchase_date: Optional[date]
    created_at: datetime
    items: List[PurchaseItemResponse] = []
    
    class Config:
        from_attributes = True


# --- OCR ---

class OCRProductMatch(BaseModel):
    """Producto detectado por OCR con su match en catálogo"""
    ocr_name: str  # Nombre extraído del ticket
    ocr_quantity: int
    ocr_unit_price: float
    ocr_subtotal: float
    
    # Match con catálogo
    matched_product_id: Optional[int] = None
    matched_product_name: Optional[str] = None
    match_confidence: float = 0  # 0-1
    status: str = "review"  # 'match', 'review', 'new'


class OCRResult(BaseModel):
    """Resultado del procesamiento OCR de un ticket"""
    supplier_name: Optional[str] = None
    supplier_cuit: Optional[str] = None
    ticket_date: Optional[date] = None
    ticket_number: Optional[str] = None
    items: List[OCRProductMatch] = []
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    raw_text: str = ""  # Texto crudo extraído
    image_path: str = ""


class OCRPurchaseCreate(BaseModel):
    """Schema para crear compra desde OCR (después de revisión)"""
    ocr_result: OCRResult
    confirmed_items: List[PurchaseItemCreate]
    supplier_id: Optional[int] = None
    notes: Optional[str] = None
