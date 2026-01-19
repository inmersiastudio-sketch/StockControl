'use client';

import { useAuthStore } from '@/store/auth-store';
import { 
  Package, 
  ShoppingCart, 
  TrendingUp, 
  AlertTriangle,
  DollarSign,
  BarChart3
} from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuthStore();

  // TODO: Obtener datos reales del backend
  const stats = {
    totalProducts: 0,
    lowStockProducts: 0,
    todaySales: 0,
    todayRevenue: 0,
  };

  return (
    <div className="space-y-6">
      {/* Saludo */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          ¡Hola, {user?.full_name || 'Usuario'}!
        </h1>
        <p className="text-gray-500 mt-1">
          Bienvenido a StockControl. Aquí tienes un resumen de tu negocio.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Productos"
          value={stats.totalProducts}
          icon={Package}
          color="primary"
        />
        <StatCard
          title="Stock Bajo"
          value={stats.lowStockProducts}
          icon={AlertTriangle}
          color="warning"
        />
        <StatCard
          title="Ventas Hoy"
          value={stats.todaySales}
          icon={ShoppingCart}
          color="success"
        />
        <StatCard
          title="Ingresos Hoy"
          value={`$${stats.todayRevenue.toLocaleString('es-AR')}`}
          icon={DollarSign}
          color="success"
        />
      </div>

      {/* Accesos rápidos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Panel de acciones rápidas */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Acciones Rápidas</h2>
          <div className="grid grid-cols-2 gap-4">
            <QuickAction
              title="Nueva Venta"
              description="Registrar una venta"
              href="/ventas/nueva"
              icon={ShoppingCart}
            />
            <QuickAction
              title="Ver Productos"
              description="Gestionar catálogo"
              href="/productos"
              icon={Package}
            />
            <QuickAction
              title="Reportes"
              description="Ver estadísticas"
              href="/reportes"
              icon={BarChart3}
            />
            <QuickAction
              title="Stock Bajo"
              description="Productos a reponer"
              href="/productos?stock_bajo=true"
              icon={AlertTriangle}
            />
          </div>
        </div>

        {/* Alertas */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Alertas</h2>
          <div className="space-y-3">
            <p className="text-gray-500 text-center py-8">
              No hay alertas por el momento 🎉
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

// Componente para las cards de estadísticas
function StatCard({
  title,
  value,
  icon: Icon,
  color,
}: {
  title: string;
  value: string | number;
  icon: any;
  color: 'primary' | 'success' | 'warning' | 'danger';
}) {
  const colorClasses = {
    primary: 'bg-primary-50 text-primary-600',
    success: 'bg-success-50 text-success-500',
    warning: 'bg-warning-50 text-warning-500',
    danger: 'bg-danger-50 text-danger-500',
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <div className={`p-3 rounded-xl ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}

// Componente para acciones rápidas
function QuickAction({
  title,
  description,
  href,
  icon: Icon,
}: {
  title: string;
  description: string;
  href: string;
  icon: any;
}) {
  return (
    <a
      href={href}
      className="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-primary-500 hover:bg-primary-50 transition-colors"
    >
      <div className="p-2 bg-primary-100 rounded-lg">
        <Icon className="w-5 h-5 text-primary-600" />
      </div>
      <div>
        <p className="font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-500">{description}</p>
      </div>
    </a>
  );
}
