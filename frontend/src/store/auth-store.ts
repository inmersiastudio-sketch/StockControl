import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi } from '@/lib/api';

interface User {
  id: number;
  username: string;
  full_name: string;
  role: 'admin' | 'employee';
  is_active: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  
  // Actions
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (username: string, password: string) => {
        // Paso 1: Login para obtener token
        const loginResponse = await authApi.login(username, password);
        const { access_token } = loginResponse.data;
        
        // Guardar token en localStorage (para api.ts interceptor)
        localStorage.setItem('token', access_token);
        
        // Paso 2: Obtener datos del usuario
        const userResponse = await authApi.me();
        const user = userResponse.data;
        
        set({
          user,
          token: access_token,
          isAuthenticated: true,
        });
      },

      logout: () => {
        localStorage.removeItem('token');
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
