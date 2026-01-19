"""
Modelos de Caja - Importados desde archivos separados para compatibilidad
"""

# Los modelos ahora están en archivos separados
# Este archivo se mantiene para compatibilidad con imports existentes

from app.models.cash_movement import CashMovement
from app.models.cash_closure import CashClosure

__all__ = ["CashMovement", "CashClosure"]
