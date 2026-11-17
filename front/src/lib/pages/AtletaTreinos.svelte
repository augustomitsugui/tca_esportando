<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import Vazio from '../components/Vazio.svelte'
  import * as treinosApi from '../api/treinos.api'
  import * as vinculosApi from '../api/vinculos.api'
  import { mensagemDeErro } from '../api/http'
  import type { Treino, TreinoAgenda } from '../models/treino.model'
  import type { AtletaEsporte } from '../models/vinculo.model'
  import { auth } from '../state/auth.svelte'
  import { formatarDataHora } from '../utils/formatar'

  let aba = $state<'proximos' | 'todos'>('proximos')
  let proximos = $state<TreinoAgenda[]>([])
  let todos = $state<Treino[]>([])
  let esportes = $state<AtletaEsporte[]>([])
  let carregando = $state(true)
  let erro = $state('')

  function nomeDoEsporte(id: string): string {
    return esportes.find((e) => e.esporte_id === id)?.esporte_nome ?? 'Esporte'
  }

  async function carregar() {
    const atletaId = auth.usuario?.profile_id
    if (!atletaId) {
      erro = 'Perfil de atleta não encontrado para esta conta.'
      carregando = false
      return
    }
    try {
      const [agenda, lista, aprovados] = await Promise.all([
        treinosApi.proximosDoAtleta(atletaId),
        treinosApi.doAtleta(atletaId),
        vinculosApi.meusEsportes(),
      ])
      proximos = agenda
      todos = lista
      esportes = aprovados
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Meus treinos" subtitulo="Treinos dos esportes em que você foi aprovado." />

<div class="space-y-4">
  <Alert tipo="erro" mensagem={erro} />

  <div class="inline-flex rounded-lg border border-slate-200 bg-white p-1">
    <button
      class="rounded-md px-4 py-1.5 text-sm font-semibold {aba === 'proximos'
        ? 'bg-emerald-600 text-white'
        : 'text-slate-600'}"
      onclick={() => (aba = 'proximos')}
    >
      Próximos
    </button>
    <button
      class="rounded-md px-4 py-1.5 text-sm font-semibold {aba === 'todos'
        ? 'bg-emerald-600 text-white'
        : 'text-slate-600'}"
      onclick={() => (aba = 'todos')}
    >
      Todos
    </button>
  </div>

  {#if carregando}
    <Loading />
  {:else if aba === 'proximos'}
    {#if proximos.length === 0}
      <Vazio texto="Nenhum treino futuro marcado." />
    {:else}
      <div class="grid gap-4 sm:grid-cols-2">
        {#each proximos as treino (treino.treino_id)}
          <div class="cartao">
            <p class="text-xs font-semibold uppercase tracking-wide text-emerald-600">
              {treino.esporte_nome}
            </p>
            <h3 class="mt-1 text-lg font-bold text-slate-900">{treino.treino_nome}</h3>
            <p class="mt-2 text-sm text-slate-600">📅 {formatarDataHora(treino.data_hora)}</p>
            <p class="text-sm text-slate-600">📍 {treino.local_nome}</p>
            <p class="text-sm text-slate-600">🧑‍🏫 {treino.treinador_nome}</p>
          </div>
        {/each}
      </div>
    {/if}
  {:else if todos.length === 0}
    <Vazio texto="Nenhum treino encontrado para os seus esportes." />
  {:else}
    <div class="cartao overflow-x-auto p-0 sm:p-0">
      <table class="tabela">
        <thead>
          <tr>
            <th>Treino</th>
            <th>Esporte</th>
            <th>Data e hora</th>
            <th>Descrição</th>
          </tr>
        </thead>
        <tbody>
          {#each todos as treino (treino.id)}
            <tr>
              <td class="font-medium text-slate-900">{treino.nome}</td>
              <td>{nomeDoEsporte(treino.esporte_id)}</td>
              <td class="whitespace-nowrap">{formatarDataHora(treino.data_hora)}</td>
              <td class="text-slate-500">{treino.descricao ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>
