"""
Modelo de Cierre de Caja Diario
"""

from sqlalchemy import Column, Integer, Float, Date, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class CashClosure(Base):
    __tablename__ = "cash_closures"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    expected_cash = Column(Float, nullable=False)  # Efectivo esperado según sistema
    counted_cash = Column(Float, nullable=False)  # Efectivo contado físicamente
    difference = Column(Float, nullable=False)  # counted - expected
    notes = Column(Text, nullable=True)  # Observaciones
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    user = relationship("User", back_populates="cash_closures")

    @property
    def has_difference(self):
        """Si hay diferencia significativa"""
        return abs(self.difference) > 0.01

    def __repr__(self):
        return f"<CashClosure(id={self.id}, date={self.date}, difference={self.difference})>"
