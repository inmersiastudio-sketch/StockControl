'use client';

export default function VentasPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Ventas</h1>
          <p className="text-gray-500">Historial de ventas</p>
        </div>
        <button className="btn-primary">
          + Nueva Venta
        </button>
      </div>

      {/* TODO: Lista de ventas - Implementar en Sprint 2 */}
      <div className="card">
        <p className="text-gray-500 text-center py-12">
          Historial de ventas - En desarrollo (Sprint 2)
        </p>
      </div>
    </div>
  );
}
