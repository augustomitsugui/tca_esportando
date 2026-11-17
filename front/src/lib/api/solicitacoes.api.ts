// src/lib/api/solicitacoes.api.ts
// Solicitações de cargo (treinador e coordenador)
import { requisitar } from './http'
import type { NovaSolicitacao, RoleRequest } from '../models/solicitacao.model'

export function minhas(): Promise<RoleRequest[]> {
  return requisitar<RoleRequest[]>('/role-requests/me')
}

export function pendentesDoCoordenador(): Promise<RoleRequest[]> {
  return requisitar<RoleRequest[]>('/role-requests/pending/coordinator')
}

export function historicoDoCoordenador(): Promise<RoleRequest[]> {
  return requisitar<RoleRequest[]>('/role-requests/coordinator/history')
}

export function pendentesDoAdmin(): Promise<RoleRequest[]> {
  return requisitar<RoleRequest[]>('/role-requests/pending/superadmin')
}

export function aprovar(id: string): Promise<RoleRequest> {
  return requisitar<RoleRequest>(`/role-requests/${id}/approve`, { metodo: 'POST' })
}

// O backend exige o motivo da recusa.
export function rejeitar(id: string, motivo: string): Promise<RoleRequest> {
  return requisitar<RoleRequest>(`/role-requests/${id}/reject`, {
    metodo: 'POST',
    corpo: { rejection_reason: motivo },
  })
}

export function enviarNova(dados: NovaSolicitacao): Promise<RoleRequest> {
  return requisitar<RoleRequest>('/role-requests', { metodo: 'POST', corpo: dados })
}
