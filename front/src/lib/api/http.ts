// src/lib/api/http.ts
// Única porta de saída para a API. Cuida de: endereço, token JWT e erros.

// "/api" é repassado pelo proxy do Vite (veja vite.config.ts)
const URL_BASE: string = import.meta.env.VITE_API_URL ?? '/api'
const CHAVE_TOKEN = 'tca_token'

// ---------- Token ----------
// O token fica no sessionStorage: some quando a aba é fechada.
// (O backend só aceita "Authorization: Bearer", então não dá para usar cookie httpOnly.)
export function lerToken(): string | null {
  try {
    return sessionStorage.getItem(CHAVE_TOKEN)
  } catch {
    return null
  }
}

export function salvarToken(token: string): void {
  try {
    sessionStorage.setItem(CHAVE_TOKEN, token)
  } catch {
    /* sem armazenamento: o usuário terá que entrar de novo ao recarregar */
  }
}

export function apagarToken(): void {
  try {
    sessionStorage.removeItem(CHAVE_TOKEN)
  } catch {
    /* ignora */
  }
}

// ---------- Erros ----------
export class ApiError extends Error {
  status: number

  constructor(mensagem: string, status: number) {
    super(mensagem)
    this.status = status
  }
}

const TRADUCOES: Record<string, string> = {
  LOGIN_BAD_CREDENTIALS: 'E-mail ou senha incorretos.',
  LOGIN_USER_NOT_VERIFIED: 'Este usuário ainda não foi verificado.',
  REGISTER_USER_ALREADY_EXISTS: 'Este e-mail já está cadastrado.',
  Unauthorized: 'Sua sessão expirou. Entre novamente.',
}

// O backend responde {"detail": "texto"} (erros de negócio)
// ou {"detail": [{loc, msg}, ...]} (erros de validação, status 422).
function extrairMensagem(corpo: unknown, status: number): string {
  if (corpo && typeof corpo === 'object' && 'detail' in corpo) {
    const detail = (corpo as { detail: unknown }).detail
    if (typeof detail === 'string') return TRADUCOES[detail] ?? detail
    if (Array.isArray(detail)) {
      return detail
        .map((item) => {
          const msg = typeof item?.msg === 'string' ? item.msg : 'valor inválido'
          const campo = Array.isArray(item?.loc) ? item.loc.slice(1).join('.') : ''
          return campo ? `${campo}: ${msg}` : msg
        })
        .join(' | ')
    }
  }
  if (status === 401) return 'Sua sessão expirou. Entre novamente.'
  if (status === 403) return 'Você não tem permissão para esta ação.'
  if (status === 404) return 'Registro não encontrado.'
  if (status >= 500) return 'Erro no servidor. Tente novamente mais tarde.'
  return 'Não foi possível concluir a ação.'
}

export function mensagemDeErro(erro: unknown): string {
  return erro instanceof Error ? erro.message : 'Ocorreu um erro inesperado.'
}

// ---------- Sessão expirada ----------
// Quem controla a sessão (auth.svelte.ts) registra aqui o que fazer no erro 401.
let aoExpirar: (() => void) | null = null

export function definirAoExpirar(funcao: () => void): void {
  aoExpirar = funcao
}

// ---------- Requisição ----------
interface Opcoes {
  metodo?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  corpo?: unknown // enviado como JSON
  formulario?: Record<string, string> // enviado como x-www-form-urlencoded (login)
  autenticado?: boolean // padrão: true (envia o token)
}

export async function requisitar<T>(caminho: string, opcoes: Opcoes = {}): Promise<T> {
  const { metodo = 'GET', corpo, formulario, autenticado = true } = opcoes

  const cabecalhos: Record<string, string> = {}
  let body: string | undefined

  if (formulario) {
    cabecalhos['Content-Type'] = 'application/x-www-form-urlencoded'
    body = new URLSearchParams(formulario).toString()
  } else if (corpo !== undefined) {
    cabecalhos['Content-Type'] = 'application/json'
    body = JSON.stringify(corpo)
  }

  const token = lerToken()
  if (autenticado && token) cabecalhos['Authorization'] = `Bearer ${token}`

  let resposta: Response
  try {
    resposta = await fetch(`${URL_BASE}${caminho}`, { method: metodo, headers: cabecalhos, body })
  } catch {
    throw new ApiError('Não foi possível conectar ao servidor. Verifique se a API está rodando.', 0)
  }

  if (resposta.status === 204) return undefined as T

  let dados: unknown = null
  try {
    dados = await resposta.json()
  } catch {
    dados = null
  }

  if (!resposta.ok) {
    // Token inválido ou expirado: limpa a sessão e volta para o login.
    if (resposta.status === 401 && autenticado && token && aoExpirar) aoExpirar()
    throw new ApiError(extrairMensagem(dados, resposta.status), resposta.status)
  }

  return dados as T
}
