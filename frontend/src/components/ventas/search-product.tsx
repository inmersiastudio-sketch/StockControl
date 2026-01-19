'use client';

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { productsApi } from '@/lib/api';
import { Input } from '@/components/ui/input';
import { Search, Loader2 } from 'lucide-react';
import type { Product } from '@/types';

interface SearchProductProps {
  onResults: (products: Product[]) => void;
}

export function SearchProduct({ onResults }: SearchProductProps) {
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);

    return () => clearTimeout(timer);
  }, [search]);

  const { data: response, isLoading } = useQuery({
    queryKey: ['products', debouncedSearch],
    queryFn: () => productsApi.list({ search: debouncedSearch || undefined }),
    enabled: debouncedSearch.length > 0,
  });

  // Enviar resultados al padre cuando cambian
  useEffect(() => {
    if (response?.data) {
      onResults(response.data);
    } else if (debouncedSearch.length === 0) {
      onResults([]);
    }
  }, [response?.data, debouncedSearch, onResults]);

  // Manejar atajo de teclado F3
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'F3') {
        e.preventDefault();
        document.getElementById('search-products')?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="space-y-2">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
        <Input
          id="search-products"
          type="text"
          placeholder="Buscar por nombre, código o escanear código de barras..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-10 h-12 text-base"
          autoFocus
        />
        {isLoading && (
          <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 animate-spin text-primary" />
        )}
      </div>

      <div className="text-xs text-muted-foreground">
        💡 Tip: Presioná <kbd className="px-1.5 py-0.5 bg-gray-200 rounded text-xs">F3</kbd> para buscar rápido
      </div>
    </div>
  );
}
