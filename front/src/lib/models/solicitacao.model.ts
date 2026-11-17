// src/lib/models/solicitacao.model.ts
import type { Papel, StatusSolicitacao } from './user.model'

export interface RoleRequest {
  id: string
  user_id: string
  requested_role: Exclude<Papel, 'atleta'>
  status: StatusSolicitacao
  institution_id: string | null
  institution_name: string | null
  institution_description: string | null
  institution_latitude: number | null
  institution_longitude: number | null
  decided_by: string | null
  created_at: string
  decided_at: string | null
  rejection_reason: string | null
}

export interface NovaSolicitacao {
  requested_role: Exclude<Papel, 'atleta'>
  institution_id?: string | null
  institution_name?: string | null
  institution_description?: string | null
  institution_latitude?: number | null
  institution_longitude?: number | null
}
