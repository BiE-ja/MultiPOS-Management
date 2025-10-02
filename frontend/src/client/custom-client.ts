// frontend/src/client/custom-client.ts

import axios, { isAxiosError } from 'axios'; 
import type {
  AxiosError,
  AxiosRequestConfig,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios';
import z, { ZodError } from 'zod';


// Utilise import.meta.env dans le contexte Vite, sinon fallback à process.env (Node)
const BASE_URL = typeof window !== 'undefined'
  ? (import.meta.env?.VITE_API_URL || 'http://localhost:8000')
  : process.env.VITE_API_URL || 'http://localhost:8000'; // 🔁 Configurable



// 🔐 Fonction pour récupérer dynamiquement le token d'accès
// get Access Token from localStorage
// Make sure to set the access token in localStorage after login
// e.g., localStorage.setItem('access_token', 'your_access_token_here');
function getAccessToken(): string | null {
  return localStorage.getItem('access_token');
}

// 🛡️ Fonction optionnelle pour rafraîchir le token (à implémenter selon ton backend)
async function refreshAccessToken(): Promise<void> {
  const refreshToken = localStorage.getItem('refresh_token');
  
  if (!refreshToken) throw new Error('No refresh token available');

  try {
    const response = await axios.post(`${BASE_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    });
    localStorage.setItem('access_token', response.data.access_token);
  } catch (err) {
    console.error('Failed to refresh token:', err);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = "/login"; // 🔁 Rediriger vers login si besoin
  }
}

// 💅 Client Axios personnalisé
const instance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Utile pour les cookies cross-domain
});

// 🧠 Intercepteur de requêtes — ajoute automatiquement le token
instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    if (import.meta.env.DEV) {
      console.log('[Request]', config.method?.toUpperCase(), config.url);
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ❤️ Intercepteur de réponses — gère les erreurs et tente un refresh si 401
instance.interceptors.response.use(
  (response: AxiosResponse) => {
    if (import.meta.env.DEV) {
      console.log('[Response]', response.status, response.config.url);
    }
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // 👇 Si token expiré, tente de rafraîchir
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        await refreshAccessToken();
        const newToken = getAccessToken();
        if (newToken) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return instance(originalRequest); // 🔁 Retente la requête
        }
      } catch (refreshError) {
        console.error("Session expirée. Redirection…");
        window.location.href = "/login"; // Redirection vers la page de connexion
        return Promise.reject(refreshError);
      }
    }

    // 🔥 Log de l’erreur
    handleRequestError(error);
    return Promise.reject(error);
  }
);

type MutationFnArgs<TVariables= unknown>={
  url: string;
  method: AxiosRequestConfig['method'];
  body?:TVariables;
  params?: AxiosRequestConfig["params"];
} & Omit<AxiosRequestConfig, 'url'|'method'|'data'|'params'>;

export const customAxios  = async<TData = unknown, TVariables = unknown>(
  {url, method, body, params, ...config}: MutationFnArgs<TVariables>):Promise<TData>=>{
    const response = await instance.request<TData>({
      url,
      method,
      data: body,
      params,
      ...config,
  });

  return response.data;
}

export type APIErrorType<Error> = AxiosError<Error>;

// 🛡️ Fonction pour gérer les erreurs 
export function handleRequestError(error: unknown) {
  if (isAxiosError(error)) {
    throw error.response?.data;
  }

  if (error instanceof ZodError) {
    console.error(z.treeifyError(error));
  }

  console.log(error);

  throw error;
}

