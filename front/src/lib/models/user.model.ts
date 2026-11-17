

export type Papel = 'atleta' | 'treinador' | 'coordenador'

export type StatusSolicitacao = 'pendente' | 'aprovada' | 'rejeitada'

export interface Me {
  id: string
  email: string
  is_active: boolean
  is_superuser: boolean // true = ADMIN
  is_verified: boolean
  role: Papel // o ADMIN também vem como atleta: use is_superuser
  approval_status: StatusSolicitacao | null
  institution_id: string | null
  profile_id: string | null // id do perfil (atleta, treinador ou coordenador)
}

export interface TokenResposta {
  access_token: string
  token_type: string
}
