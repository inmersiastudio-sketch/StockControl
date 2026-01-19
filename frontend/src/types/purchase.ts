/**
 * Types de Compra y OCR
 */

export interface PurchaseItem {
  id: number;
  product_id: number;
  product_name: string;
  product_code: string;
  quantity: number;
  unit_cost: number;
  subtotal: number;
  expiration_date?: string;
}

export interface Purchase {
  id: number;
  supplier_id?: number;
  supplier_name?: string;
  total: number;
  notes?: string;
  receipt_image_path?: string;
  user_id: number;
  user_name: string;
  purchase_date?: string;
  created_at: string;
  items: PurchaseItem[];
}

export interface PurchaseItemCreate {
  product_id: number;
  quantity: number;
  unit_cost: number;
  expiration_date?: string;
}

export interface PurchaseCreate {
  supplier_id?: number;
  items: PurchaseItemCreate[];
  notes?: string;
  purchase_date?: string;
}

// OCR Types
export interface OCRProductMatch {
  ocr_name: string;
  ocr_quantity: number;
  ocr_unit_price: number;
  ocr_subtotal: number;
  matched_product_id?: number;
  matched_product_name?: string;
  match_confidence: number;
  status: 'match' | 'review' | 'new';
}

export interface OCRResult {
  supplier_name?: string;
  supplier_cuit?: string;
  ticket_date?: string;
  ticket_number?: string;
  items: OCRProductMatch[];
  subtotal?: number;
  tax?: number;
  total?: number;
  raw_text: string;
  image_path: string;
}

export interface Supplier {
  id: number;
  name: string;
  cuit?: string;
  phone?: string;
  email?: string;
  address?: string;
  notes?: string;
  is_active: boolean;
  total_purchases: number;
  total_spent: number;
  created_at: string;
}
