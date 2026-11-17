// src/lib/models/treino.model.ts

export interface Treino {
  id: string
  nome: string
  descricao: string | null
  data_hora: string // ISO 8601
  treinador_id: string
  local_id: string
  esporte_id: string
}

export interface TreinoForm {
  nome: string
  descricao: string | null
  data_hora: string
  treinador_id: string
  local_id: string
  esporte_id: string
}

// GET /atletas/{id}/proximos-treinos
export interface TreinoAgenda {
  treino_id: string
  treino_nome: string
  esporte_nome: string
  data_hora: string
  treinador_nome: string
  local_nome: string
}
