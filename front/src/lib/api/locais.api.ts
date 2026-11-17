// src/lib/api/locais.api.ts
import { requisitar } from './http'
import type { Local, LocalForm, LocalInstituicao } from '../models/local.model'
import type { Esporte } from '../models/esporte.model'

// Coordenador
export function listar(): Promise<Local[]> {
  return requisitar<Local[]>('/locais')
}

export function criar(dados: LocalForm): Promise<Local> {
  return requisitar<Local>('/locais', { metodo: 'POST', corpo: dados })
}

export function atualizar(id: string, dados: LocalForm): Promise<Local> {
  return requisitar<Local>(`/locais/${id}`, { metodo: 'PUT', corpo: dados })
}

export function excluir(id: string): Promise<void> {
  return requisitar<void>(`/locais/${id}`, { metodo: 'DELETE' })
}

// Treinador: locais ligados à instituição dele
export function listarDoTreinador(): Promise<Local[]> {
  return requisitar<Local[]>('/treinadores/me/locais')
}

// Vínculo local <-> instituição
export function listarInstituicoes(localId: string): Promise<LocalInstituicao[]> {
  return requisitar<LocalInstituicao[]>(`/locais/${localId}/instituicoes`)
}

export function vincularInstituicao(localId: string, instituicaoId: string): Promise<LocalInstituicao> {
  return requisitar<LocalInstituicao>(`/locais/${localId}/instituicoes/${instituicaoId}`, { metodo: 'POST' })
}

export function desvincularInstituicao(localId: string, instituicaoId: string): Promise<void> {
  return requisitar<void>(`/locais/${localId}/instituicoes/${instituicaoId}`, { metodo: 'DELETE' })
}

// Vínculo local <-> esporte
export function listarEsportes(localId: string): Promise<Esporte[]> {
  return requisitar<Esporte[]>(`/locais/${localId}/esportes`)
}

export function vincularEsporte(localId: string, esporteId: string): Promise<void> {
  return requisitar<void>(`/locais/${localId}/esportes/${esporteId}`, { metodo: 'POST' })
}

export function desvincularEsporte(localId: string, esporteId: string): Promise<void> {
  return requisitar<void>(`/locais/${localId}/esportes/${esporteId}`, { metodo: 'DELETE' })
}
