'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { PageBanner } from '@/components/layout/page-banner';
import { SearchProduct } from '@/components/ventas/search-product';
import { ProductCard } from '@/components/ventas/product-card';
import { Cart } from '@/components/ventas/cart';
import api from '@/lib/api';
import { useCartStore } from '@/store/cart-store';
import { useAuthStore } from '@/store/auth-store';
import { toast } from 'sonner';
import { Product } from '@/types';

export default function VentasPage() {
  const [searchResults, setSearchResults] = useState<Product[]>([]);
  const { items, addItem, clearCart } = useCartStore();
  const { user } = useAuthStore();
  const queryClient = useQueryClient();

  // Mutación para crear venta
  const createSaleMutation = useMutation({
    mutationFn: async (saleData: {
      items: { product_id: number; quantity: number }[];
      discount: number;
      payment_method: string;
      notes?: string;
    }) => {
      const response = await api.post('/sales/', saleData);
      return response.data;
    },
    onSuccess: (data) => {
      toast.success(`¡Venta #${data.id} registrada exitosamente!`, {
        description: `Total: $${data.total.toFixed(2)}`
      });
      clearCart();
      // Invalidar cache de productos para actualizar stock
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || 'Error al procesar la venta';
      toast.error('Error en la venta', { description: message });
    }
  });

  const handleSearchResults = (products: Product[]) => {
    setSearchResults(products);
  };

  const handleAddToCart = (product: Product) => {
    addItem(product);
    toast.success(`${product.name} agregado al carrito`);
  };

  const handleConfirmSale = async (
    paymentMethod: string,
    discount: number,
    amountPaid?: number
  ) => {
    if (items.length === 0) {
      toast.error('El carrito está vacío');
      return;
    }

    const saleData = {
      items: items.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity
      })),
      discount,
      payment_method: paymentMethod,
      notes: amountPaid ? `Cliente pagó: $${amountPaid}` : undefined
    };

    await createSaleMutation.mutateAsync(saleData);
  };

  return (
    <div className="space-y-6">
      <PageBanner
        title="💰 Punto de Venta"
        description={`Bienvenido ${user?.full_name || 'Cajero'}. Buscá productos con F3 o hacé click en el buscador.`}
        color="green"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Columna izquierda: Búsqueda y productos */}
        <div className="lg:col-span-2 space-y-4">
          <SearchProduct onResults={handleSearchResults} />

          {searchResults.length > 0 && (
            <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
              {searchResults.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAdd={handleAddToCart}
                />
              ))}
            </div>
          )}

          {searchResults.length === 0 && (
            <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed">
              <p className="text-muted-foreground text-lg">
                🔍 Buscá productos por nombre o código
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Presioná <kbd className="px-2 py-1 bg-gray-200 rounded text-xs">F3</kbd> para enfocar el buscador
              </p>
            </div>
          )}
        </div>

        {/* Columna derecha: Carrito */}
        <div className="lg:col-span-1">
          <div className="sticky top-6">
            <Cart
              onConfirmSale={handleConfirmSale}
              loading={createSaleMutation.isPending}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
