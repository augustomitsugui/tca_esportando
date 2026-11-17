import { tokenStorage } from './tokenStorage.js';

// O Vite repassa /api/* para o backend (veja vite.config.js).
const BASE = '/api';

let onUnauthorized = () => {};
export const setUnauthorizedHandler = (fn) => {
  onUnauthorized = fn;
};

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

// códigos do fastapi-users traduzidos para a tela
const KNOWN_CODES = {
  LOGIN_BAD_CREDENTIALS: 'E-mail ou senha incorretos.',
  LOGIN_USER_NOT_VERIFIED: 'Esta conta ainda não foi verificada.',
  REGISTER_USER_ALREADY_EXISTS: 'Já existe uma conta com este e-mail.',
  Unauthorized: 'Sua sessão expirou. Entre novamente.',
};

function parseDetail(data, fallback) {
  const detail = data?.detail;
  if (typeof detail === 'string') return KNOWN_CODES[detail] ?? detail;
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg).filter(Boolean).join(' · ') || fallback;
  }
  if (detail && typeof detail === 'object' && detail.code) {
    return KNOWN_CODES[detail.code] ?? detail.reason ?? fallback;
  }
  return fallback;
}

export function errorMessage(err) {
  return err instanceof ApiError
    ? err.message
    : 'Algo deu errado. Tente novamente.';
}

async function request(method, path, { body, form, auth = true } = {}) {
  const headers = {};
  const token = tokenStorage.get();
  if (auth && token) headers.Authorization = `Bearer ${token}`;

  let payload;
  if (form) {
    headers['Content-Type'] = 'application/x-www-form-urlencoded';
    payload = new URLSearchParams(form).toString();
  } else if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
    payload = JSON.stringify(body);
  }

  let res;
  try {
    res = await fetch(`${BASE}${path}`, { method, headers, body: payload });
  } catch {
    throw new ApiError('Não foi possível conectar ao servidor.', 0);
  }

  if (res.status === 204) return null;

  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = null;
  }

  if (!res.ok) {
    if (res.status === 401 && auth && token) onUnauthorized();
    throw new ApiError(
      parseDetail(data, res.statusText || 'Erro inesperado.'),
      res.status,
      data,
    );
  }
  return data;
}

export const api = {
  get: (path, opts) => request('GET', path, opts),
  post: (path, body, opts) => request('POST', path, { ...opts, body }),
  put: (path, body, opts) => request('PUT', path, { ...opts, body }),
  del: (path, opts) => request('DELETE', path, opts),
  form: (path, form, opts) => request('POST', path, { ...opts, form }),
};
