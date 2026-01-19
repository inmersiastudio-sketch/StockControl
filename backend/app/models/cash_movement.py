"""
Modelo de Movimiento de Caja (ingresos y egresos)
"""

from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class CashMovement(Base):
    __tablename__ = "cash_movements"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False, index=True)  # 'income' o 'expense'
    amount = Column(Float, nullable=False)
    method = Column(String(20), nullable=False)  # 'cash', 'card', 'transfer'
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relaciones
    user = relationship("User", back_populates="cash_movements")

    def __repr__(self):
        return f"<CashMovement(id={self.id}, type='{self.type}', amount={self.amount})>"
