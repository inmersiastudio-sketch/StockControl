"""
Schemas Pydantic - Import centralizado
"""

from .auth import Token, TokenData, LoginRequest
from .user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserWithStats,
    UserRole,
    UserPasswordChange,
)
from .category import CategoryCreate, CategoryResponse
from .supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from .product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductWithLots,
    ProductLotResponse,
    ProductSearch,
)
from .purchase import (
    PurchaseCreate,
    PurchaseResponse,
    PurchaseItemCreate,
    PurchaseItemResponse,
    OCRProductMatch,
    OCRResult,
    OCRPurchaseCreate,
)
from .sale import (
    SaleCreate,
    SaleResponse,
    SaleItemCreate,
    SaleItemResponse,
    SaleCancelRequest,
    SaleSearch,
    PaymentMethod,
)
from .cash import (
    CashMovementCreate,
    CashMovementResponse,
    CashClosureCreate,
    CashClosureResponse,
    CashSummary,
)
from .report import DailySummary, TopProduct, AlertProduct

__all__ = [
    # Auth
    "Token",
    "TokenData",
    "LoginRequest",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserWithStats",
    "UserRole",
    "UserPasswordChange",
    # Category
    "CategoryCreate",
    "CategoryResponse",
    # Supplier
    "SupplierCreate",
    "SupplierUpdate",
    "SupplierResponse",
    # Product
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductWithLots",
    "ProductLotResponse",
    "ProductSearch",
    # Purchase
    "PurchaseCreate",
    "PurchaseResponse",
    "PurchaseItemCreate",
    "PurchaseItemResponse",
    "OCRProductMatch",
    "OCRResult",
    "OCRPurchaseCreate",
    # Sale
    "SaleCreate",
    "SaleResponse",
    "SaleItemCreate",
    "SaleItemResponse",
    "SaleCancelRequest",
    "SaleSearch",
    "PaymentMethod",
    # Cash
    "CashMovementCreate",
    "CashMovementResponse",
    "CashClosureCreate",
    "CashClosureResponse",
    "CashSummary",
    # Report
    "DailySummary",
    "TopProduct",
    "AlertProduct",
]
