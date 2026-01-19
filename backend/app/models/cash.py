"""
Modelos de Caja: Movimientos y Cierres de Caja
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CashMovement(Base):
    """
    Movimiento de caja (ingreso o egreso).
    Las ventas no se registran aquí, solo movimientos adicionales.
    """
    __tablename__ = "cash_movements"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    type = Column(String(20), nullable=False)  # 'income' o 'expense'
    amount = Column(Float, nullable=False)
    method = Column(String(20), nullable=False)  # 'cash', 'card', 'transfer'
    description = Column(Text, nullable=False)
    
    # Usuario que realizó el movimiento
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación
    user = relationship("User")
    
    def __repr__(self):
        return f"<CashMovement {self.type}: ${self.amount}>"


class CashClosure(Base):
    """
    Cierre de caja diario.
    Registra el arqueo de caja con el conteo de billetes.
    """
    __tablename__ = "cash_closures"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    date = Column(Date, nullable=False, unique=True)  # Solo un cierre por día
    
    # Montos
    expected_cash = Column(Float, nullable=False)  # Lo que debería haber según sistema
    counted_cash = Column(Float, nullable=False)  # Lo que se contó físicamente
    difference = Column(Float, nullable=False)  # counted - expected
    
    # Detalle del conteo de billetes (JSON)
    # Ej: {"1000": 5, "500": 10, "200": 3, ...}
    bills_count = Column(JSON, nullable=True)
    
    # Resumen del día
    total_sales_cash = Column(Float, default=0)
    total_sales_card = Column(Float, default=0)
    total_sales_transfer = Column(Float, default=0)
    total_incomes = Column(Float, default=0)  # Ingresos adicionales
    total_expenses = Column(Float, default=0)  # Egresos
    
    notes = Column(Text, nullable=True)
    
    # Usuario que hizo el cierre
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación
    user = relationship("User")
    
    def __repr__(self):
        return f"<CashClosure {self.date}: diff ${self.difference}>"
