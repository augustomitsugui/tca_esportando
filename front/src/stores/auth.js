import { writable } from 'svelte/store';
import { authService } from '../services/authService.js';
import { tokenStorage } from '../services/tokenStorage.js';
import { setUnauthorizedHandler } from '../services/api.js';
import { navigate } from '../router/router.js';

export const session = writable({ ready: false, user: null });

// Carrega o usuário a partir do token salvo (ao abrir o app)
export async function bootstrap() {
  if (!tokenStorage.get()) {
    session.set({ ready: true, user: null });
    return;
  }
  try {
    const user = await authService.me();
    session.set({ ready: true, user });
  } catch {
    tokenStorage.clear();
    session.set({ ready: true, user: null });
  }
}

// Recarrega /auth/me (ex.: depois de uma aprovação)
export async function refreshUser() {
  const user = await authService.me();
  session.update((s) => ({ ...s, user }));
  return user;
}

export async function signIn(email, password) {
  const { access_token } = await authService.login(email, password);
  tokenStorage.set(access_token);
  try {
    const user = await authService.me();
    session.set({ ready: true, user });
    return user;
  } catch (err) {
    tokenStorage.clear();
    throw err;
  }
}

export function signOut() {
  tokenStorage.clear();
  session.set({ ready: true, user: null });
  navigate('/login', { replace: true });
}

// token vencido/inválido: volta para o login
setUnauthorizedHandler(signOut);
