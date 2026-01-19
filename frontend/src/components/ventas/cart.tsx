'use client';

import { useState } from 'react';
import { useCartStore } from '@/store/cart-store';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Separator } from '@/components/ui/separator';
import { formatCurrency } from '@/lib/utils';
import { Trash2, Minus, Plus, ShoppingCart } from 'lucide-react';

interface CartProps {
  onConfirmSale: (paymentMethod: string, discount: number, amountPaid?: number) => void;
  loading?: boolean;
}

export function Cart({ onConfirmSale, loading }: CartProps) {
  const { items, updateQuantity, removeItem, clearCart } = useCartStore();
  
  const [paymentMethod, setPaymentMethod] = useState<'cash' | 'card' | 'transfer'>('cash');
  const [discount, setDiscount] = useState(0);
  const [amountPaid, setAmountPaid] = useState<number>(0);

  // Calcular totales
  const subtotal = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);
  const total = subtotal - discount;
  const change = paymentMethod === 'cash' ? Math.max(0, amountPaid - total) : 0;

  const handleConfirm = () => {
    onConfirmSale(
      paymentMethod,
      discount,
      paymentMethod === 'cash' ? amountPaid : undefined
    );
  };

  const canConfirm = total > 0 && (paymentMethod !== 'cash' || amountPaid >= total);

  if (items.length === 0) {
    return (
      <div className="border rounded-lg p-6 bg-gray-50">
        <div className="text-center py-8 text-muted-foreground">
          <ShoppingCart className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p className="font-medium">El carrito está vacío</p>
          <p className="text-sm">Buscá y agregá productos para comenzar</p>
        </div>
      </div>
    );
  }

  return (
    <div className="border rounded-lg p-4 bg-white space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold flex items-center gap-2">
          <ShoppingCart className="w-5 h-5" />
          Carrito ({totalItems})
        </h2>
        <Button
          variant="ghost"
          size="sm"
          onClick={clearCart}
          className="text-danger-500 hover:text-danger-600"
        >
          Limpiar
        </Button>
      </div>

      <div className="space-y-2 max-h-[250px] overflow-y-auto pr-2">
        {items.map((item) => (
          <div key={item.product.id} className="border rounded-lg p-3 bg-gray-50">
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1 min-w-0">
                <h3 className="font-medium text-sm truncate">{item.product.name}</h3>
                <p className="text-sm text-success-500 font-bold">
                  {formatCurrency(item.product.price)} c/u
                </p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeItem(item.product.id)}
                className="shrink-0 text-danger-500 hover:text-danger-600 h-8 w-8 p-0"
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>

            <div className="flex items-center justify-between mt-2">
              <div className="flex items-center gap-1">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                  className="h-8 w-8 p-0"
                >
                  <Minus className="w-3 h-3" />
                </Button>
                <Input
                  type="number"
                  value={item.quantity}
                  onChange={(e) => updateQuantity(item.product.id, parseInt(e.target.value) || 1)}
                  className="w-14 text-center h-8"
                  min={1}
                  max={item.product.current_stock}
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                  disabled={item.quantity >= item.product.current_stock}
                  className="h-8 w-8 p-0"
                >
                  <Plus className="w-3 h-3" />
                </Button>
              </div>
              <span className="font-bold text-lg">
                {formatCurrency(item.product.price * item.quantity)}
              </span>
            </div>
          </div>
        ))}
      </div>

      <Separator />

      <div className="space-y-3">
        <div className="flex justify-between text-sm">
          <span>Subtotal:</span>
          <span className="font-medium">{formatCurrency(subtotal)}</span>
        </div>

        <div className="space-y-2">
          <Label className="text-xs">Descuento (opcional)</Label>
          <Input
            type="number"
            value={discount || ''}
            onChange={(e) => setDiscount(Math.min(parseFloat(e.target.value) || 0, subtotal))}
            placeholder="0"
            min={0}
            max={subtotal}
            className="h-9"
          />
        </div>

        {discount > 0 && (
          <div className="flex justify-between text-sm text-danger-500">
            <span>Descuento:</span>
            <span className="font-medium">-{formatCurrency(discount)}</span>
          </div>
        )}

        <div className="flex justify-between text-2xl font-bold text-success-600 bg-success-50 p-3 rounded-lg">
          <span>TOTAL:</span>
          <span>{formatCurrency(total)}</span>
        </div>
      </div>

      <Separator />

      <div className="space-y-3">
        <Label className="font-semibold">Método de Pago</Label>
        <RadioGroup 
          value={paymentMethod} 
          onValueChange={(v: 'cash' | 'card' | 'transfer') => setPaymentMethod(v)}
          className="grid grid-cols-3 gap-2"
        >
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="cash" id="cash" />
            <Label htmlFor="cash" className="cursor-pointer text-sm">💵 Efectivo</Label>
          </div>
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="card" id="card" />
            <Label htmlFor="card" className="cursor-pointer text-sm">💳 Tarjeta</Label>
          </div>
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="transfer" id="transfer" />
            <Label htmlFor="transfer" className="cursor-pointer text-sm">📱 Transfer</Label>
          </div>
        </RadioGroup>
      </div>

      {paymentMethod === 'cash' && (
        <div className="space-y-2 bg-primary-50 p-4 rounded-lg border border-primary-200">
          <Label className="font-semibold">Cliente paga con:</Label>
          <Input
            type="number"
            value={amountPaid || ''}
            onChange={(e) => setAmountPaid(parseFloat(e.target.value) || 0)}
            placeholder={total.toString()}
            className="text-lg font-bold h-12"
            autoFocus={paymentMethod === 'cash'}
          />
          {amountPaid >= total && (
            <div className="text-2xl font-bold text-success-600 text-center py-2 bg-white rounded-lg">
              🎉 Vuelto: {formatCurrency(change)}
            </div>
          )}
          {amountPaid > 0 && amountPaid < total && (
            <div className="text-sm text-danger-500 text-center">
              Faltan {formatCurrency(total - amountPaid)}
            </div>
          )}
        </div>
      )}

      <Separator />

      <div className="space-y-2">
        <Button
          className="w-full h-12 text-lg font-bold"
          onClick={handleConfirm}
          disabled={loading || !canConfirm}
        >
          {loading ? 'Procesando...' : '✅ CONFIRMAR VENTA'}
        </Button>
        <Button
          variant="outline"
          className="w-full"
          onClick={clearCart}
          disabled={loading}
        >
          Cancelar
        </Button>
      </div>
    </div>
  );
}
