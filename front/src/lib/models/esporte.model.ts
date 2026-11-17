// src/lib/models/esporte.model.ts

export interface Esporte {
  id: string
  nome: string
  descricao: string | null
  instituicao_id: string | null
}

export interface EsporteForm {
  nome: string
  descricao: string | null
}
