// src/lib/api/auth.api.ts
import { requisitar } from './http'
import type { Me, TokenResposta } from '../models/user.model'

// O login é diferente dos outros: o backend espera formulário (não JSON),
// com o e-mail no campo "username".
export function login(email: string, senha: string): Promise<TokenResposta> {
  return requisitar<TokenResposta>('/auth/jwt/login', {
    metodo: 'POST',
    formulario: { username: email, password: senha },
    autenticado: false,
  })
}

export function buscarUsuario(): Promise<Me> {
  return requisitar<Me>('/auth/me')
}

// ---------- Cadastros ----------
interface DadosBase {
  email: string
  password: string
  nome: string
  bio: string | null
}

export interface CadastroAtleta extends DadosBase {
  ano: number
}

export interface CadastroTreinador extends DadosBase {
  institution_id: string
}

export interface CadastroCoordenador extends DadosBase {
  institution_name: string
  institution_description: string | null
  institution_latitude: number | null
  institution_longitude: number | null
}

export function cadastrarAtleta(dados: CadastroAtleta): Promise<unknown> {
  return requisitar('/auth/register/athlete', { metodo: 'POST', corpo: dados, autenticado: false })
}

export function cadastrarTreinador(dados: CadastroTreinador): Promise<unknown> {
  return requisitar('/auth/register/trainer', { metodo: 'POST', corpo: dados, autenticado: false })
}

export function cadastrarCoordenador(dados: CadastroCoordenador): Promise<unknown> {
  return requisitar('/auth/register/coordinator', { metodo: 'POST', corpo: dados, autenticado: false })
}
