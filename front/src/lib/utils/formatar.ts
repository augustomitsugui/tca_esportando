// src/lib/utils/formatar.ts
// Pequenas funções de apoio para datas e campos opcionais dos formulários.

export function formatarDataHora(iso: string): string {
  return new Date(iso).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
}

export function formatarData(iso: string): string {
  return new Date(iso).toLocaleDateString('pt-BR')
}

// ISO (vindo da API) -> "2026-11-20T18:30", formato do <input type="datetime-local">
export function paraInputLocal(iso: string): string {
  const d = new Date(iso)
  const dois = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${dois(d.getMonth() + 1)}-${dois(d.getDate())}T${dois(d.getHours())}:${dois(d.getMinutes())}`
}

// "2026-11-20T18:30" (horário local) -> ISO em UTC, com fuso definido (o backend usa fuso)
export function deInputLocal(valor: string): string {
  return new Date(valor).toISOString()
}

// Campo vazio vira null (o backend aceita null nos campos opcionais)
export function textoOuNull(valor: string): string | null {
  const texto = valor.trim()
  return texto === '' ? null : texto
}

export function numeroOuNull(valor: string): number | null {
  const texto = valor.trim().replace(',', '.')
  if (texto === '') return null
  const numero = Number(texto)
  return Number.isNaN(numero) ? null : numero
}

// Mostra só o começo de um UUID (a API de solicitações não devolve o nome do solicitante)
export function idCurto(id: string): string {
  return id.slice(0, 8)
}
