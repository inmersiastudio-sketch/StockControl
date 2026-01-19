/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // Para deployment local/Tauri
  reactStrictMode: true,
  // Configuración para desarrollo local con backend
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
