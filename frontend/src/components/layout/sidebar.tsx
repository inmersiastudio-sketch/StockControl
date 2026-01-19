'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuthStore } from '@/store/auth-store';
import {
  Package,
  ShoppingCart,
  Truck,
  BarChart3,
  Settings,
  Users,
  Wallet,
  LayoutDashboard,
  ScanLine,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const menuItems = [
  {
    title: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
    roles: ['admin', 'employee'],
  },
  {
    title: 'Ventas',
    href: '/ventas',
    icon: ShoppingCart,
    roles: ['admin', 'employee'],
  },
  {
    title: 'Productos',
    href: '/productos',
    icon: Package,
    roles: ['admin', 'employee'],
  },
  {
    title: 'Compras',
    href: '/compras',
    icon: ScanLine,
    roles: ['admin'],
  },
  {
    title: 'Proveedores',
    href: '/proveedores',
    icon: Truck,
    roles: ['admin'],
  },
  {
    title: 'Caja',
    href: '/caja',
    icon: Wallet,
    roles: ['admin'],
  },
  {
    title: 'Reportes',
    href: '/reportes',
    icon: BarChart3,
    roles: ['admin'],
  },
  {
    title: 'Usuarios',
    href: '/usuarios',
    icon: Users,
    roles: ['admin'],
  },
  {
    title: 'Configuración',
    href: '/configuracion',
    icon: Settings,
    roles: ['admin'],
  },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuthStore();
  const userRole = user?.role || 'employee';

  // Filtrar items según el rol
  const visibleItems = menuItems.filter((item) =>
    item.roles.includes(userRole)
  );

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Logo */}
      <div className="h-16 flex items-center px-6 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
            <Package className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-xl text-gray-900">StockControl</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
        {visibleItems.map((item) => {
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              )}
            >
              <item.icon
                className={cn(
                  'w-5 h-5',
                  isActive ? 'text-primary-600' : 'text-gray-400'
                )}
              />
              {item.title}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <p className="text-xs text-gray-400 text-center">
          StockControl v1.0.0
        </p>
      </div>
    </aside>
  );
}
