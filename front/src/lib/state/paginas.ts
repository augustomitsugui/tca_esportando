// src/lib/state/paginas.ts
// Controle de acesso VISUAL: quais telas cada perfil pode abrir.
// Atenção: isto só esconde telas. Quem realmente protege os dados é o backend.

import type { Perfil } from './auth.svelte'

export const paginasPublicas = ['login', 'cadastro']

export const paginasPorPerfil: Record<Perfil, string[]> = {
  atleta: ['inicio', 'esportes', 'treinos'],
  treinador: ['inicio', 'esportes', 'treinos', 'atletas'],
  coordenador: ['inicio', 'solicitacoes', 'instituicao', 'locais'],
  admin: ['inicio', 'solicitacoes', 'instituicoes'],
  pendente: ['inicio'],
}

// Dada a página pedida no endereço, devolve a página que realmente pode ser mostrada.
export function resolverPagina(pedida: string, perfil: Perfil | null): string {
  if (perfil === null) {
    return paginasPublicas.includes(pedida) ? pedida : 'login'
  }
  return paginasPorPerfil[perfil].includes(pedida) ? pedida : 'inicio'
}
