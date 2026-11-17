// src/lib/state/auth.svelte.ts
// Guarda quem está logado. Usa $state (runes do Svelte 5), como na aula.

import type { Me } from '../models/user.model'
import * as authApi from '../api/auth.api'
import { apagarToken, definirAoExpirar, lerToken, salvarToken } from '../api/http'
import { router } from './router.svelte'

// "pendente" = treinador/coordenador que ainda não foi aprovado (ou foi recusado)
export type Perfil = 'atleta' | 'treinador' | 'coordenador' | 'admin' | 'pendente'

class AuthState {
  usuario = $state<Me | null>(null)
  iniciando = $state(true) // true enquanto confere se já existe sessão
  aviso = $state('') // mensagem mostrada na tela de login

  // Perfil usado para decidir o dashboard e as telas permitidas
  perfil: Perfil | null = $derived.by(() => {
    const u = this.usuario
    if (!u) return null
    if (u.is_superuser) return 'admin' // o ADMIN vem com role "atleta"
    if (u.role === 'atleta') return 'atleta'
    if (u.approval_status === 'aprovada') return u.role
    return 'pendente'
  })

  // Chamado uma vez ao abrir o site: se há token salvo, busca o usuário.
  async iniciar() {
    definirAoExpirar(() => {
      this.aviso = 'Sua sessão expirou. Entre novamente.'
      this.limparSessao()
    })
    if (lerToken()) {
      try {
        this.usuario = await authApi.buscarUsuario()
      } catch {
        apagarToken()
        this.usuario = null
      }
    }
    this.iniciando = false
  }

  async entrar(email: string, senha: string) {
    const resposta = await authApi.login(email, senha)
    salvarToken(resposta.access_token)
    try {
      this.usuario = await authApi.buscarUsuario()
    } catch (erro) {
      apagarToken()
      throw erro
    }
  }

  // Recarrega os dados (ex.: depois de ser aprovado)
  async atualizar() {
    this.usuario = await authApi.buscarUsuario()
  }

  // O JWT não tem "logout" no servidor: sair é apagar o token daqui.
  sair() {
    this.aviso = ''
    this.limparSessao()
  }

  private limparSessao() {
    apagarToken()
    this.usuario = null
    router.navegar('login')
  }
}

export const auth = new AuthState()
