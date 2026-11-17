// src/lib/api/instituicoes.api.ts
import { requisitar } from './http'
import type { Instituicao, InstituicaoForm, InstituicaoPublica } from '../models/instituicao.model'

// Pública: usada no cadastro de treinador (ainda sem login)
export function listarPublicas(): Promise<InstituicaoPublica[]> {
  return requisitar<InstituicaoPublica[]>('/instituicoes/public', { autenticado: false })
}

// Coordenador: só a própria instituição. ADMIN: todas.
export function listar(): Promise<Instituicao[]> {
  return requisitar<Instituicao[]>('/instituicoes')
}

export function atualizar(id: string, dados: InstituicaoForm): Promise<Instituicao> {
  return requisitar<Instituicao>(`/instituicoes/${id}`, { metodo: 'PUT', corpo: dados })
}

export function excluir(id: string): Promise<void> {
  return requisitar<void>(`/instituicoes/${id}`, { metodo: 'DELETE' })
}
