"""
Servicio de matching de productos
Compara nombres del OCR con el catálogo existente
TODO: Implementar en Sprint 5
"""

from difflib import SequenceMatcher
import unicodedata
import re
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductMatcher:
    """
    Servicio para hacer matching entre nombres de productos
    extraídos por OCR y el catálogo existente
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_best_match(
        self, 
        ocr_name: str, 
        min_confidence: float = 0.8
    ) -> dict:
        """
        Encontrar el mejor match en el catálogo para un nombre de OCR
        
        Args:
            ocr_name: Nombre extraído del ticket
            min_confidence: Umbral mínimo de confianza (0-1)
            
        Returns:
            {
                'product': Product o None,
                'confidence': float,
                'status': 'match' | 'review' | 'new'
            }
        """
        products = self.db.query(Product).filter(Product.is_active == True).all()
        
        if not products:
            return {
                'product': None,
                'confidence': 0,
                'status': 'new'
            }
        
        normalized_ocr = self._normalize_name(ocr_name)
        
        best_match = None
        best_score = 0
        
        for product in products:
            # Comparar con nombre
            score_name = self._calculate_similarity(
                normalized_ocr, 
                self._normalize_name(product.name)
            )
            
            # Comparar con código si existe
            score_code = 0
            if product.code:
                score_code = self._calculate_similarity(
                    normalized_ocr,
                    self._normalize_name(product.code)
                )
            
            score = max(score_name, score_code)
            
            if score > best_score:
                best_score = score
                best_match = product
        
        # Determinar status
        if best_score >= min_confidence:
            status = 'match'
        elif best_score >= 0.5:
            status = 'review'
        else:
            status = 'new'
        
        return {
            'product': best_match,
            'confidence': round(best_score, 2),
            'status': status
        }
    
    def find_suggestions(
        self, 
        ocr_name: str, 
        limit: int = 5
    ) -> List[dict]:
        """
        Encontrar múltiples sugerencias ordenadas por similitud
        """
        products = self.db.query(Product).filter(Product.is_active == True).all()
        normalized_ocr = self._normalize_name(ocr_name)
        
        scored_products = []
        for product in products:
            score = self._calculate_similarity(
                normalized_ocr,
                self._normalize_name(product.name)
            )
            scored_products.append({
                'product': product,
                'confidence': round(score, 2)
            })
        
        # Ordenar por score descendente
        scored_products.sort(key=lambda x: x['confidence'], reverse=True)
        
        return scored_products[:limit]
    
    def _normalize_name(self, name: str) -> str:
        """
        Normalizar nombre para comparación
        - Convertir a minúsculas
        - Remover acentos
        - Remover caracteres especiales
        - Remover espacios extra
        """
        if not name:
            return ""
        
        # Minúsculas
        name = name.lower()
        
        # Remover acentos
        name = ''.join(
            c for c in unicodedata.normalize('NFD', name)
            if unicodedata.category(c) != 'Mn'
        )
        
        # Remover caracteres especiales excepto espacios
        name = re.sub(r'[^a-z0-9\s]', '', name)
        
        # Remover espacios extra
        name = ' '.join(name.split())
        
        return name
    
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """
        Calcular similitud entre dos strings (0-1)
        Usa el algoritmo de SequenceMatcher
        """
        if not s1 or not s2:
            return 0
        
        return SequenceMatcher(None, s1, s2).ratio()
