// src/lib/models/instituicao.model.ts

export interface Instituicao {
  id: string
  nome: string
  descricao: string | null
  latitude: number | null
  longitude: number | null
}

// GET /instituicoes/public devolve só estes dois campos
export interface InstituicaoPublica {
  id: string
  nome: string
}

export interface InstituicaoForm {
  nome: string
  descricao: string | null
  latitude: number | null
  longitude: number | null
}
