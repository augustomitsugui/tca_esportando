import { writable } from 'svelte/store';

// Roteador por caminho usando a History API: URLs limpas (/login, /admin

const read = () => ({
  path: window.location.pathname.replace(/(.)\/+$/, '$1'),
  search: window.location.search,
});

export const location = writable(read());

export function navigate(to, { replace = false } = {}) {
  const current = window.location.pathname + window.location.search;
  if (to !== current) {
    window.history[replace ? 'replaceState' : 'pushState']({}, '', to);
  }
  location.set(read());
  if (!replace) window.scrollTo({ top: 0 });
}

window.addEventListener('popstate', () => location.set(read()));

export function matchRoute(routes, path) {
  return routes.find((route) => route.path === path) ?? null;
}
