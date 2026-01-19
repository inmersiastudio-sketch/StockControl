/**
 * Exportar todos los types
 */

export * from './user';
export * from './product';
export * from './sale';
export * from './purchase';

// Types genéricos
export interface ApiError {
  detail: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}
