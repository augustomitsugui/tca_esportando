import { api } from './api.js';

// Vínculos de um local com esportes e instituições
export const localService = {
  sports: (localId) => api.get(`/locais/${localId}/esportes`),
  linkSport: (localId, esporteId) =>
    api.post(`/locais/${localId}/esportes/${esporteId}`),
  unlinkSport: (localId, esporteId) =>
    api.del(`/locais/${localId}/esportes/${esporteId}`),

  institutions: (localId) => api.get(`/locais/${localId}/instituicoes`),
  linkInstitution: (localId, instituicaoId) =>
    api.post(`/locais/${localId}/instituicoes/${instituicaoId}`),
  unlinkInstitution: (localId, instituicaoId) =>
    api.del(`/locais/${localId}/instituicoes/${instituicaoId}`),
};
