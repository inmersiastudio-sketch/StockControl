import axios from 'axios';

// Crear instancia de axios con configuración base
// Usamos URL relativa para aprovechar el proxy de Next.js en desarrollo
const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token a las peticiones
api.interceptors.request.use(
  (config) => {
    // Obtener token del localStorage
    const token = typeof window !== 'undefined' 
      ? localStorage.getItem('token') 
      : null;
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de respuesta
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Si es error 401, limpiar token y redirigir a login
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// --- Funciones de API ---

// Auth
export const authApi = {
  login: (username: string, password: string) => {
    // OAuth2 requiere form-urlencoded
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
  
  me: () => api.get('/auth/me'),
  
  registerAdmin: (data: { username: string; password: string; full_name: string }) =>
    api.post('/auth/register-admin', data),
};

// Products
export const productsApi = {
  list: (params?: { search?: string; category_id?: number; low_stock?: boolean }) =>
    api.get('/products', { params }),
  
  get: (id: number) => api.get(`/products/${id}`),
  
  create: (data: any) => api.post('/products', data),
  
  update: (id: number, data: any) => api.patch(`/products/${id}`, data),
  
  delete: (id: number) => api.delete(`/products/${id}`),
};

// Categories
export const categoriesApi = {
  list: () => api.get('/categories'),
  create: (data: { name: string; description?: string }) => api.post('/categories', data),
  update: (id: number, data: any) => api.patch(`/categories/${id}`, data),
  delete: (id: number) => api.delete(`/categories/${id}`),
};

// Suppliers
export const suppliersApi = {
  list: () => api.get('/suppliers'),
  get: (id: number) => api.get(`/suppliers/${id}`),
  create: (data: any) => api.post('/suppliers', data),
  update: (id: number, data: any) => api.patch(`/suppliers/${id}`, data),
  delete: (id: number) => api.delete(`/suppliers/${id}`),
};

// Sales
export const salesApi = {
  list: (params?: any) => api.get('/sales', { params }),
  get: (id: number) => api.get(`/sales/${id}`),
  create: (data: any) => api.post('/sales', data),
  cancel: (id: number, data: { reason: string }) => api.post(`/sales/${id}/cancel`, data),
};

// Purchases
export const purchasesApi = {
  list: () => api.get('/purchases'),
  get: (id: number) => api.get(`/purchases/${id}`),
  create: (data: any) => api.post('/purchases', data),
  processOCR: (formData: FormData) => api.post('/purchases/ocr', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
};

// Cash
export const cashApi = {
  getSummary: () => api.get('/cash/summary'),
  createMovement: (data: any) => api.post('/cash/movement', data),
  closeCash: (data: any) => api.post('/cash/close', data),
};

// Reports
export const reportsApi = {
  daily: (date?: string) => api.get('/reports/daily', { params: { date } }),
  period: (dateFrom: string, dateTo: string) =>
    api.get('/reports/period', { params: { date_from: dateFrom, date_to: dateTo } }),
  alerts: () => api.get('/reports/alerts'),
};

// Users
export const usersApi = {
  list: () => api.get('/users'),
  get: (id: number) => api.get(`/users/${id}`),
  create: (data: any) => api.post('/users', data),
  update: (id: number, data: any) => api.patch(`/users/${id}`, data),
  delete: (id: number) => api.delete(`/users/${id}`),
};
