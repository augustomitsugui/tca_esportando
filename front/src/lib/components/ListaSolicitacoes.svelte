<script lang="ts">
  import Vazio from './Vazio.svelte'
  import StatusBadge from './StatusBadge.svelte'
  import type { RoleRequest } from '../models/solicitacao.model'
  import { formatarDataHora, idCurto } from '../utils/formatar'

  // Lista de solicitações com os botões Aprovar / Recusar.
  // Quem usa o componente diz o que fazer ao aprovar e ao recusar.
  let {
    itens,
    podeDecidir = true,
    textoVazio = 'Nenhuma solicitação.',
    aoAprovar,
    aoRejeitar,
  }: {
    itens: RoleRequest[]
    podeDecidir?: boolean
    textoVazio?: string
    aoAprovar: (id: string) => Promise<void>
    aoRejeitar: (id: string, motivo: string) => Promise<void>
  } = $props()

  let ocupadoId = $state('')
  let recusandoId = $state('') // solicitação que está pedindo o motivo da recusa
  let motivo = $state('')

  async function aprovar(item: RoleRequest) {
    ocupadoId = item.id
    try {
      await aoAprovar(item.id)
    } finally {
      ocupadoId = ''
    }
  }

  async function confirmarRecusa(item: RoleRequest) {
    if (motivo.trim() === '') return
    ocupadoId = item.id
    try {
      await aoRejeitar(item.id, motivo.trim())
      recusandoId = ''
      motivo = ''
    } catch {
      // A tela que usou o componente já mostra o erro; o campo continua aberto.
    } finally {
      ocupadoId = ''
    }
  }

  function abrirRecusa(item: RoleRequest) {
    recusandoId = item.id
    motivo = ''
  }
</script>

{#if itens.length === 0}
  <Vazio texto={textoVazio} />
{:else}
  <ul class="space-y-3">
    {#each itens as item (item.id)}
      <li class="rounded-xl border border-slate-200 p-4">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div class="min-w-0">
            <div class="flex flex-wrap items-center gap-2">
              <p class="font-semibold capitalize text-slate-900">{item.requested_role}</p>
              <StatusBadge status={item.status} />
            </div>
            {#if item.institution_name}
              <p class="mt-1 text-sm text-slate-700">
                Instituição: <span class="font-medium">{item.institution_name}</span>
              </p>
            {/if}
            {#if item.institution_description}
              <p class="text-sm text-slate-500">{item.institution_description}</p>
            {/if}
            <p class="mt-1 text-xs text-slate-400">
              Usuário {idCurto(item.user_id)} · enviada em {formatarDataHora(item.created_at)}
            </p>
            {#if item.status === 'rejeitada' && item.rejection_reason}
              <p class="mt-1 text-sm text-red-700">Motivo da recusa: {item.rejection_reason}</p>
            {/if}
          </div>

          {#if podeDecidir && item.status === 'pendente' && recusandoId !== item.id}
            <div class="flex gap-2">
              <button
                class="btn-primario btn-pequeno"
                disabled={ocupadoId === item.id}
                onclick={() => aprovar(item)}
              >
                Aprovar
              </button>
              <button
                class="btn-perigo btn-pequeno"
                disabled={ocupadoId === item.id}
                onclick={() => abrirRecusa(item)}
              >
                Recusar
              </button>
            </div>
          {/if}
        </div>

        {#if recusandoId === item.id}
          <div class="mt-3 space-y-2 rounded-lg bg-slate-50 p-3">
            <label class="block">
              <span class="rotulo">Motivo da recusa (obrigatório)</span>
              <textarea class="campo" rows="2" maxlength="500" bind:value={motivo}></textarea>
            </label>
            <div class="flex gap-2">
              <button
                class="btn-perigo btn-pequeno"
                disabled={motivo.trim() === '' || ocupadoId === item.id}
                onclick={() => confirmarRecusa(item)}
              >
                Confirmar recusa
              </button>
              <button class="btn-claro btn-pequeno" onclick={() => (recusandoId = '')}>Voltar</button>
            </div>
          </div>
        {/if}
      </li>
    {/each}
  </ul>
{/if}
