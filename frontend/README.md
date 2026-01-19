# StockControl Frontend
# Sistema de Inventario para Despensas y Almacenes

## Requisitos

- Node.js 18+
- npm o pnpm

## Instalación

1. Instalar dependencias:
```bash
npm install
```

2. Crear archivo de entorno (opcional):
```bash
cp .env.example .env.local
```

3. Ejecutar servidor de desarrollo:
```bash
npm run dev
```

4. Abrir en el navegador:
http://localhost:3000

## Estructura del proyecto

```
frontend/
├── src/
│   ├── app/                 # App Router de Next.js 14
│   │   ├── (dashboard)/     # Páginas del dashboard (protegidas)
│   │   ├── login/           # Página de login
│   │   └── layout.tsx       # Layout principal
│   ├── components/          # Componentes reutilizables
│   │   ├── layout/          # Sidebar, Header
│   │   └── ui/              # Componentes de UI (botones, inputs, etc.)
│   ├── lib/                 # Utilidades y API client
│   └── store/               # Estado global con Zustand
├── public/                  # Archivos estáticos
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## Scripts disponibles

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Build de producción
- `npm run start` - Iniciar servidor de producción
- `npm run lint` - Ejecutar linter
