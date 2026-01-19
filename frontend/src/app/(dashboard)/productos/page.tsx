'use client';

export default function ProductosPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Productos</h1>
          <p className="text-gray-500">Gestiona el catálogo de productos</p>
        </div>
        <button className="btn-primary">
          + Nuevo Producto
        </button>
      </div>

      {/* TODO: Tabla de productos - Implementar en Sprint 1/2 */}
      <div className="card">
        <p className="text-gray-500 text-center py-12">
          Tabla de productos - En desarrollo
        </p>
      </div>
    </div>
  );
}
