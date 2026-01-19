/**
 * Types de Producto
 */

export interface Product {
  id: number;
  code: string;
  barcode?: string;
  name: string;
  description?: string;
  category_id?: number;
  category_name?: string;
  cost: number;
  price: number;
  min_stock: number;
  current_stock: number;
  margin_percentage: number;
  is_active: boolean;
  created_at: string;
  next_expiration?: string;
}

export interface ProductLot {
  id: number;
  quantity: number;
  initial_quantity: number;
  cost: number;
  expiration_date?: string;
  created_at: string;
  is_expired: boolean;
}

export interface ProductWithLots extends Product {
  lots: ProductLot[];
}

export interface ProductCreate {
  code: string;
  barcode?: string;
  name: string;
  description?: string;
  category_id?: number;
  cost: number;
  price: number;
  min_stock?: number;
}

export interface ProductUpdate {
  code?: string;
  barcode?: string;
  name?: string;
  description?: string;
  category_id?: number;
  cost?: number;
  price?: number;
  min_stock?: number;
  is_active?: boolean;
}

export interface Category {
  id: number;
  name: string;
  description?: string;
  product_count: number;
  created_at: string;
}
