// src/lib/api/treinos.api.ts
import { requisitar } from './http'
import type { Treino, TreinoAgenda, TreinoForm } from '../models/treino.model'

// Treinador
export function listar(): Promise<Treino[]> {
  return requisitar<Treino[]>('/treinos')
}

export function criar(dados: TreinoForm): Promise<Treino> {
  return requisitar<Treino>('/treinos', { metodo: 'POST', corpo: dados })
}

// Sempre enviamos TODOS os campos: o backend trata campo ausente como "apagar".
export function atualizar(id: string, dados: TreinoForm): Promise<Treino> {
  return requisitar<Treino>(`/treinos/${id}`, { metodo: 'PUT', corpo: dados })
}

export function excluir(id: string): Promise<void> {
  return requisitar<void>(`/treinos/${id}`, { metodo: 'DELETE' })
}

// Atleta (o id é o profile_id de /auth/me)
export function doAtleta(atletaId: string): Promise<Treino[]> {
  return requisitar<Treino[]>(`/atletas/${atletaId}/treinos`)
}

export function proximosDoAtleta(atletaId: string): Promise<TreinoAgenda[]> {
  return requisitar<TreinoAgenda[]>(`/atletas/${atletaId}/proximos-treinos`)
}
