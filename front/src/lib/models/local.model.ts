// src/lib/models/local.model.ts

export interface Local {
  id: string
  nome: string
  descricao: string | null
}

export interface LocalForm {
  nome: string
  descricao: string | null
}

export interface LocalInstituicao {
  id: string
  local_id: string
  instituicao_id: string
}
