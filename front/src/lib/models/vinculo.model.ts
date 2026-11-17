// src/lib/models/vinculo.model.ts
// Vínculo entre atleta e esporte (o atleta pede, o treinador decide)

export type StatusVinculo = 'pendente' | 'aprovado' | 'recusado'

export interface AtletaEsporte {
  id: string
  atleta_id: string
  esporte_id: string
  status: StatusVinculo
  atleta_nome: string | null
  esporte_nome: string | null
}
