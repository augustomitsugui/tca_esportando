import { api } from './api.js';

// Vínculo atleta <-> esporte
export const vinculoService = {
  // lado do atleta
  available: () => api.get('/atletas/me/esportes/disponiveis'),
  request: (esporteId) =>
    api.post(`/atletas/me/esportes/${esporteId}/solicitacoes`),
  pending: () => api.get('/atletas/me/solicitacoes-esporte'),
  approved: () => api.get('/atletas/me/esportes'),
  cancel: (vinculoId) =>
    api.del(`/atletas/me/solicitacoes-esporte/${vinculoId}`),

  // lado do treinador
  trainerPending: () => api.get('/treinadores/me/solicitacoes-esporte'),
  trainerAthletes: () => api.get('/treinadores/me/atletas'),
  decide: (vinculoId, status) =>
    api.post(`/treinadores/me/solicitacoes-esporte/${vinculoId}/decisao`, {
      status,
    }),
};
