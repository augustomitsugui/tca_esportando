import { api } from './api.js';

// Treinos do ponto de vista do atleta
export const treinoService = {
  upcoming: (atletaId) => api.get(`/atletas/${atletaId}/proximos-treinos`),
  all: (atletaId) => api.get(`/atletas/${atletaId}/treinos`),
};
