import { api } from './api.js';

export const roleRequestService = {
  mine: () => api.get('/role-requests/me'),
  pendingForCoordinator: () => api.get('/role-requests/pending/coordinator'),
  coordinatorHistory: () => api.get('/role-requests/coordinator/history'),
  pendingForAdmin: () => api.get('/role-requests/pending/superadmin'),
  approve: (id) => api.post(`/role-requests/${id}/approve`),
  reject: (id, reason) =>
    api.post(`/role-requests/${id}/reject`, { rejection_reason: reason }),
};
