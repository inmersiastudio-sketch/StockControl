import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { formatCurrency, getStockColor } from '@/lib/utils';
import { Plus } from 'lucide-react';
import type { Product } from '@/types';

interface ProductCardProps {
  product: Product;
  onAdd: (product: Product) => void;
}

export function ProductCard({ product, onAdd }: ProductCardProps) {
  const stockColor = getStockColor(product.current_stock, product.min_stock);
  const isLowStock = product.current_stock < product.min_stock;
  const outOfStock = product.current_stock === 0;

  return (
    <div className={`border rounded-lg p-3 transition-colors ${outOfStock ? 'bg-gray-100 opacity-60' : 'hover:bg-gray-50'}`}>
      <div className="flex items-center justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold truncate">{product.name}</h3>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs text-muted-foreground font-mono">{product.code}</span>
            {product.category_name && (
              <Badge variant="outline" className="text-xs">
                {product.category_name}
              </Badge>
            )}
          </div>
          <div className="flex items-center gap-3 mt-2">
            <span className="text-lg font-bold text-success-500">
              {formatCurrency(product.price)}
            </span>
            <span className={`text-sm font-medium ${stockColor}`}>
              Stock: {product.current_stock}
              {isLowStock && !outOfStock && ' ⚠️'}
              {outOfStock && ' ❌'}
            </span>
          </div>
        </div>

        <Button
          onClick={() => onAdd(product)}
          disabled={outOfStock}
          className="shrink-0"
          size="sm"
        >
          <Plus className="w-4 h-4 mr-1" />
          Agregar
        </Button>
      </div>
    </div>
  );
}
