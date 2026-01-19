import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Formatear moneda (ARS)
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
  }).format(amount);
}

/**
 * Formatear fecha
 */
export function formatDate(date: string | Date): string {
  return new Intl.DateTimeFormat('es-AR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(new Date(date));
}

/**
 * Formatear fecha y hora
 */
export function formatDateTime(date: string | Date): string {
  return new Intl.DateTimeFormat('es-AR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date));
}

/**
 * Obtener color según margen de ganancia
 */
export function getMarginColor(margin: number): string {
  if (margin > 30) return 'text-success-500';
  if (margin >= 10) return 'text-warning-500';
  return 'text-danger-500';
}

/**
 * Obtener color según stock
 */
export function getStockColor(current: number, min: number): string {
  if (current > min) return 'text-success-500';
  if (current === min) return 'text-warning-500';
  return 'text-danger-500';
}
