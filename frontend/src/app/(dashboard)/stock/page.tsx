'use client';

import { useQuery } from '@tanstack/react-query';
import { PageBanner } from '@/components/layout/page-banner';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import api from '@/lib/api';
import { formatCurrency } from '@/lib/utils';
import { Product } from '@/types';
import { AlertTriangle, Package, TrendingDown, Bell, RefreshCcw } from 'lucide-react';

export default function StockPage() {
  // Obtener productos
  const { data: products = [], isLoading, refetch } = useQuery<Product[]>({
    queryKey: ['products'],
    queryFn: async () => {
      const response = await api.get('/products/');
      return response.data;
    }
  });

  // Filtrar productos con stock bajo (menos que min_stock)
  const lowStockProducts = products.filter(p => p.current_stock <= p.min_stock && p.current_stock > 0);
  
  // Productos sin stock
  const outOfStockProducts = products.filter(p => p.current_stock === 0);

  // Productos OK
  const okProducts = products.filter(p => p.current_stock > p.min_stock);

  // Valor total del inventario
  const totalInventoryValue = products.reduce(
    (sum, p) => sum + p.price * p.current_stock, 
    0
  );

  if (isLoading) {
    return (
      <div className="space-y-6">
        <PageBanner
          title="📦 Control de Stock"
          description="Cargando inventario..."
          color="blue"
        />
        <div className="text-center py-12">
          <RefreshCcw className="w-8 h-8 animate-spin mx-auto text-primary-500" />
          <p className="mt-2 text-muted-foreground">Cargando productos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageBanner
        title="📦 Control de Stock"
        description="Monitoreá el inventario y recibí alertas de productos con stock bajo."
        color="blue"
      />

      {/* Resumen rápido */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-full bg-primary-100 text-primary-600">
                <Package className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Productos</p>
                <p className="text-2xl font-bold">{products.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-full bg-success-100 text-success-600">
                <TrendingDown className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Valor Inventario</p>
                <p className="text-2xl font-bold">{formatCurrency(totalInventoryValue)}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className={lowStockProducts.length > 0 ? 'border-warning-300 bg-warning-50' : ''}>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-full ${lowStockProducts.length > 0 ? 'bg-warning-200 text-warning-700' : 'bg-gray-100 text-gray-600'}`}>
                <AlertTriangle className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Stock Bajo</p>
                <p className="text-2xl font-bold">{lowStockProducts.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className={outOfStockProducts.length > 0 ? 'border-danger-300 bg-danger-50' : ''}>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-full ${outOfStockProducts.length > 0 ? 'bg-danger-200 text-danger-700' : 'bg-gray-100 text-gray-600'}`}>
                <Bell className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Sin Stock</p>
                <p className="text-2xl font-bold">{outOfStockProducts.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Alertas */}
      {outOfStockProducts.length > 0 && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>¡Productos sin stock!</AlertTitle>
          <AlertDescription>
            Hay {outOfStockProducts.length} producto(s) sin stock que requieren atención inmediata.
          </AlertDescription>
        </Alert>
      )}

      {lowStockProducts.length > 0 && (
        <Alert className="border-warning-300 bg-warning-50 text-warning-800">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Stock bajo</AlertTitle>
          <AlertDescription>
            Hay {lowStockProducts.length} producto(s) con stock bajo que deberías reponer pronto.
          </AlertDescription>
        </Alert>
      )}

      {/* Productos sin stock */}
      {outOfStockProducts.length > 0 && (
        <Card>
          <CardHeader className="bg-danger-50 border-b border-danger-200">
            <CardTitle className="text-danger-700 flex items-center gap-2">
              <Bell className="w-5 h-5" />
              Productos Sin Stock ({outOfStockProducts.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y">
              {outOfStockProducts.map((product) => (
                <div key={product.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                  <div>
                    <h3 className="font-medium">{product.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      Código: {product.code} | Mínimo requerido: {product.min_stock}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge variant="destructive" className="text-lg px-4 py-1">
                      0 unidades
                    </Badge>
                    <Button variant="outline" size="sm">
                      Reponer
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Productos con stock bajo */}
      {lowStockProducts.length > 0 && (
        <Card>
          <CardHeader className="bg-warning-50 border-b border-warning-200">
            <CardTitle className="text-warning-700 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Productos con Stock Bajo ({lowStockProducts.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y">
              {lowStockProducts.map((product) => (
                <div key={product.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
                  <div>
                    <h3 className="font-medium">{product.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      Código: {product.code} | Mínimo: {product.min_stock} | Precio: {formatCurrency(product.price)}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge variant="outline" className="text-lg px-4 py-1 bg-warning-100 text-warning-700 border-warning-300">
                      {product.current_stock} unidades
                    </Badge>
                    <Button variant="outline" size="sm">
                      Reponer
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Todos los productos */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Package className="w-5 h-5" />
            Todos los Productos ({products.length})
          </CardTitle>
          <Button variant="outline" size="sm" onClick={() => refetch()}>
            <RefreshCcw className="w-4 h-4 mr-2" />
            Actualizar
          </Button>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-y">
                <tr>
                  <th className="text-left p-4 font-medium">Producto</th>
                  <th className="text-left p-4 font-medium">Código</th>
                  <th className="text-right p-4 font-medium">Precio</th>
                  <th className="text-right p-4 font-medium">Stock</th>
                  <th className="text-right p-4 font-medium">Mínimo</th>
                  <th className="text-center p-4 font-medium">Estado</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {products.map((product) => {
                  const status = product.current_stock === 0 
                    ? 'danger' 
                    : product.current_stock <= product.min_stock 
                      ? 'warning' 
                      : 'success';
                  
                  return (
                    <tr key={product.id} className="hover:bg-gray-50">
                      <td className="p-4">
                        <span className="font-medium">{product.name}</span>
                      </td>
                      <td className="p-4 text-muted-foreground">{product.code}</td>
                      <td className="p-4 text-right font-medium">{formatCurrency(product.price)}</td>
                      <td className="p-4 text-right font-bold">{product.current_stock}</td>
                      <td className="p-4 text-right text-muted-foreground">{product.min_stock}</td>
                      <td className="p-4 text-center">
                        {status === 'danger' && (
                          <Badge variant="destructive">Sin Stock</Badge>
                        )}
                        {status === 'warning' && (
                          <Badge variant="outline" className="bg-warning-100 text-warning-700 border-warning-300">
                            Stock Bajo
                          </Badge>
                        )}
                        {status === 'success' && (
                          <Badge variant="outline" className="bg-success-100 text-success-700 border-success-300">
                            OK
                          </Badge>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
