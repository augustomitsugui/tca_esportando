const KEY = 'esportando.token';

export const tokenStorage = {
  get() {
    try {
      return localStorage.getItem(KEY);
    } catch {
      return null;
    }
  },
  set(token) {
    try {
      localStorage.setItem(KEY, token);
    } catch {
      /* sem storage disponível */
    }
  },
  clear() {
    try {
      localStorage.removeItem(KEY);
    } catch {
      /* sem storage disponível */
    }
  },
};
