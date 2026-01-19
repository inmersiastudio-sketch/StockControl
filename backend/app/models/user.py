"""
Modelo de Usuario (Admin y Empleados)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # 'admin' o 'employee'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    sales = relationship("Sale", back_populates="user", foreign_keys="Sale.user_id")
    purchases = relationship("Purchase", back_populates="user")
    cash_movements = relationship("CashMovement", back_populates="user")
    cash_closures = relationship("CashClosure", back_populates="user")
    cancelled_sales = relationship(
        "Sale",
        back_populates="cancelled_by_user",
        foreign_keys="Sale.cancelled_by",
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
