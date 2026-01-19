/**
 * Types de Venta
 */

export type PaymentMethod = 'cash' | 'card' | 'transfer';

export interface SaleItem {
  id: number;
  product_id: number;
  product_name: string;
  product_code: string;
  quantity: number;
  unit_price: number;
  unit_cost: number;
  subtotal: number;
  profit: number;
}

export interface Sale {
  id: number;
  subtotal: number;
  discount: number;
  total: number;
  payment_method: PaymentMethod;
  amount_paid?: number;
  change_given?: number;
  user_id: number;
  user_name: string;
  is_cancelled: boolean;
  cancel_reason?: string;
  created_at: string;
  items: SaleItem[];
  profit: number;
}

export interface SaleItemCreate {
  product_id: number;
  quantity: number;
}

export interface SaleCreate {
  items: SaleItemCreate[];
  payment_method: PaymentMethod;
  discount?: number;
  amount_paid?: number;
}

// Para el carrito local
export interface CartItem {
  product: {
    id: number;
    code: string;
    name: string;
    price: number;
    cost: number;
    current_stock: number;
  };
  quantity: number;
}
