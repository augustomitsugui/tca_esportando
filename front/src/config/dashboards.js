import { api } from '../services/api.js';
import { vinculoService } from '../services/vinculoService.js';
import { roleRequestService } from '../services/roleRequestService.js';
import { treinoService } from '../services/treinoService.js';

const count = (promise) => promise.then((list) => list.length);
const countOf = (path) => () => count(api.get(path));

// Cada "stat" busca uma lista no backend e mostra o tamanho.
export const dashboards = {
  atleta: {
    icon: 'directions_run',
    subtitle: 'Pronto para o próximo treino?',
    stats: [
      { label: 'Esportes aprovados', icon: 'verified', tone: 'green', load: () => count(vinculoService.approved()) },
      { label: 'Pedidos pendentes', icon: 'hourglass_top', tone: 'red', load: () => count(vinculoService.pending()) },
      { label: 'Próximos treinos', icon: 'event_upcoming', tone: 'green', load: (user) => count(treinoService.upcoming(user.profile_id)) },
    ],
  },
  treinador: {
    icon: 'sports',
    subtitle: 'Hora de montar o time.',
    stats: [
      { label: 'Pedidos de atletas', icon: 'mark_email_unread', tone: 'red', load: () => count(vinculoService.trainerPending()) },
      { label: 'Atletas vinculados', icon: 'groups', tone: 'green', load: () => count(vinculoService.trainerAthletes()) },
      { label: 'Treinos', icon: 'event', tone: 'green', load: countOf('/treinos') },
    ],
  },
  coordenador: {
    icon: 'badge',
    subtitle: 'Cuide da sua instituição.',
    stats: [
      { label: 'Treinadores aguardando', icon: 'how_to_reg', tone: 'red', load: () => count(roleRequestService.pendingForCoordinator()) },
      { label: 'Locais', icon: 'stadium', tone: 'green', load: countOf('/locais') },
      { label: 'Esportes', icon: 'sports_soccer', tone: 'green', load: countOf('/esportes/coordenador/me') },
    ],
  },
  admin: {
    icon: 'shield_person',
    subtitle: 'Visão geral de todo o Esportando.',
    stats: [
      { label: 'Solicitações pendentes', icon: 'how_to_reg', tone: 'red', load: () => count(roleRequestService.pendingForAdmin()) },
      { label: 'Instituições', icon: 'account_balance', tone: 'green', load: countOf('/instituicoes') },
      { label: 'Esportes', icon: 'sports_soccer', tone: 'green', load: countOf('/esportes') },
      { label: 'Locais', icon: 'stadium', tone: 'green', load: countOf('/locais') },
      { label: 'Treinos', icon: 'event', tone: 'green', load: countOf('/treinos') },
      { label: 'Atletas', icon: 'directions_run', tone: 'green', load: countOf('/atletas') },
    ],
  },
};
