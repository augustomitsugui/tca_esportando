// src/lib/api/vinculos.api.ts
// Vínculo atleta <-> esporte
import { requisitar } from './http'
import type { AtletaEsporte } from '../models/vinculo.model'
import type { Esporte } from '../models/esporte.model'

// ---------- Atleta ----------
export function esportesDisponiveis(): Promise<Esporte[]> {
  return requisitar<Esporte[]>('/atletas/me/esportes/disponiveis')
}

export function solicitar(esporteId: string): Promise<AtletaEsporte> {
  return requisitar<AtletaEsporte>(`/atletas/me/esportes/${esporteId}/solicitacoes`, { metodo: 'POST' })
}

export function minhasSolicitacoes(): Promise<AtletaEsporte[]> {
  return requisitar<AtletaEsporte[]>('/atletas/me/solicitacoes-esporte')
}

export function meusEsportes(): Promise<AtletaEsporte[]> {
  return requisitar<AtletaEsporte[]>('/atletas/me/esportes')
}

export function cancelar(vinculoId: string): Promise<void> {
  return requisitar<void>(`/atletas/me/solicitacoes-esporte/${vinculoId}`, { metodo: 'DELETE' })
}

// ---------- Treinador ----------
export function pendentesDoTreinador(): Promise<AtletaEsporte[]> {
  return requisitar<AtletaEsporte[]>('/treinadores/me/solicitacoes-esporte')
}

export function atletasDoTreinador(): Promise<AtletaEsporte[]> {
  return requisitar<AtletaEsporte[]>('/treinadores/me/atletas')
}

export function decidir(vinculoId: string, status: 'aprovado' | 'recusado'): Promise<AtletaEsporte> {
  return requisitar<AtletaEsporte>(`/treinadores/me/solicitacoes-esporte/${vinculoId}/decisao`, {
    metodo: 'POST',
    corpo: { status },
  })
}
