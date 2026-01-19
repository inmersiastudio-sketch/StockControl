"""
Servicio de OCR para tickets de compra
TODO: Implementar en Sprint 5
"""

import re
from typing import Optional
from datetime import datetime, date
from pathlib import Path


class ReceiptOCRService:
    """
    Servicio para procesar tickets de compra con OCR
    Usa Tesseract para la extracción de texto
    """
    
    def __init__(self):
        self.tesseract_available = self._check_tesseract()
    
    def _check_tesseract(self) -> bool:
        """Verificar si Tesseract está instalado"""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False
    
    def process_receipt(self, image_path: str) -> dict:
        """
        Pipeline completo de procesamiento de ticket
        
        Args:
            image_path: Ruta a la imagen del ticket
            
        Returns:
            Diccionario con datos estructurados del ticket
        """
        if not self.tesseract_available:
            raise RuntimeError("Tesseract no está instalado")
        
        # 1. Pre-procesar imagen
        processed_image = self._preprocess_image(image_path)
        
        # 2. Extraer texto con OCR
        raw_text = self._extract_text(processed_image)
        
        # 3. Parsear datos estructurados
        structured_data = self._parse_receipt(raw_text)
        
        # 4. Validar y limpiar
        validated_data = self._validate_data(structured_data)
        
        return validated_data
    
    def _preprocess_image(self, image_path: str):
        """
        Mejorar calidad de imagen para OCR
        - Convertir a escala de grises
        - Reducir ruido
        - Binarización adaptativa
        - Corregir rotación
        """
        # TODO: Implementar con OpenCV
        # import cv2
        # img = cv2.imread(image_path)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ...
        pass
    
    def _extract_text(self, image) -> str:
        """
        Extraer texto con Tesseract
        Configurado para español
        """
        # TODO: Implementar
        # import pytesseract
        # config = '--oem 3 --psm 6 -l spa'
        # text = pytesseract.image_to_string(image, config=config)
        return ""
    
    def _parse_receipt(self, text: str) -> dict:
        """
        Parsear texto extraído a estructura de datos
        """
        data = {
            'supplier_name': None,
            'supplier_cuit': None,
            'ticket_date': None,
            'ticket_number': None,
            'items': [],
            'subtotal': None,
            'tax': None,
            'total': None,
            'raw_text': text
        }
        
        # Extraer CUIT (formato: XX-XXXXXXXX-X)
        cuit_match = re.search(r'CUIT:?\s*(\d{2}-\d{8}-\d)', text, re.IGNORECASE)
        if cuit_match:
            data['supplier_cuit'] = cuit_match.group(1)
        
        # Extraer fecha (formato: DD/MM/YYYY)
        date_match = re.search(r'Fecha:?\s*(\d{2}/\d{2}/\d{4})', text, re.IGNORECASE)
        if date_match:
            try:
                data['ticket_date'] = datetime.strptime(
                    date_match.group(1), '%d/%m/%Y'
                ).date()
            except ValueError:
                pass
        
        # Extraer total
        total_match = re.search(r'TOTAL:?\s*\$?([\d.,]+)', text, re.IGNORECASE)
        if total_match:
            try:
                total_str = total_match.group(1).replace('.', '').replace(',', '.')
                data['total'] = float(total_str)
            except ValueError:
                pass
        
        # TODO: Implementar extracción de items
        # Patrón típico: CANTIDAD DESCRIPCIÓN PRECIO
        
        return data
    
    def _validate_data(self, data: dict) -> dict:
        """
        Validar y limpiar datos extraídos
        """
        # TODO: Implementar validaciones
        return data
