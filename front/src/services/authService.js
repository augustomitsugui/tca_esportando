import { api } from './api.js';

export const authService = {
  // fastapi-users espera form-urlencoded com "username"
  login: (email, password) =>
    api.form('/auth/jwt/login', { username: email, password }, { auth: false }),

  me: () => api.get('/auth/me'),

  register: (role, payload) => {
    const paths = {
      atleta: '/auth/register/athlete',
      treinador: '/auth/register/trainer',
      coordenador: '/auth/register/coordinator',
    };
    return api.post(paths[role], payload, { auth: false });
  },

  publicInstitutions: () => api.get('/instituicoes/public', { auth: false }),
};
