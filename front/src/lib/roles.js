// Apenas leitura de papéis para decidir ROTAS e MENUS.
// Quem autoriza de verdade é sempre o backend.

export const ROLE_LABELS = {
  atleta: 'Atleta',
  treinador: 'Treinador',
  coordenador: 'Coordenador',
  admin: 'Administrador',
};

export function getRole(user) {
  if (!user) return null;
  return user.is_superuser ? 'admin' : user.role;
}

// treinador/coordenador só entram no sistema depois de aprovados
export function needsApproval(user) {
  if (!user || user.is_superuser) return false;
  return (
    (user.role === 'treinador' || user.role === 'coordenador') &&
    user.approval_status !== 'aprovada'
  );
}

export function homePathFor(user) {
  if (!user) return '/login';
  if (user.is_superuser) return '/admin';
  if (needsApproval(user)) return '/aguardando';
  return '/painel';
}
