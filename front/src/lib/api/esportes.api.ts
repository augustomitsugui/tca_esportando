// src/lib/api/esportes.api.ts
import { requisitar } from './http'
import type { Esporte, EsporteForm } from '../models/esporte.model'

// Treinador: os esportes que ele administra
export function listarDoTreinador(): Promise<Esporte[]> {
  return requisitar<Esporte[]>('/esportes')
}

// Coordenador: os esportes da instituição dele
export function listarDoCoordenador(): Promise<Esporte[]> {
  return requisitar<Esporte[]>('/esportes/coordenador/me')
}

export function criar(dados: EsporteForm): Promise<Esporte> {
  return requisitar<Esporte>('/esportes', { metodo: 'POST', corpo: dados })
}

export function atualizar(id: string, dados: EsporteForm): Promise<Esporte> {
  return requisitar<Esporte>(`/esportes/${id}`, { metodo: 'PUT', corpo: dados })
}

export function excluir(id: string): Promise<void> {
  return requisitar<void>(`/esportes/${id}`, { metodo: 'DELETE' })
}
