import { getRole, homePathFor, needsApproval } from '../lib/roles.js';

// Decide para onde mandar o usuário. Retorna null quando pode ficar.
// access: 'public' | 'guest' (só deslogado) | 'private' (logado)
export function resolveGuard(route, user) {
  if (route.redirect) return route.redirect(user);

  if (route.access === 'guest') {
    return user ? homePathFor(user) : null;
  }

  if (route.access === 'private') {
    if (!user) return '/login';

    const pending = needsApproval(user);
    if (route.pendingOnly) return pending ? null : homePathFor(user);
    if (pending) return '/aguardando';

    if (route.roles && !route.roles.includes(getRole(user))) {
      return homePathFor(user);
    }
  }
  return null;
}
