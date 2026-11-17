<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Cartao from '../components/Cartao.svelte'
  import Loading from '../components/Loading.svelte'
  import StatusBadge from '../components/StatusBadge.svelte'
  import Titulo from '../components/Titulo.svelte'
  import Vazio from '../components/Vazio.svelte'
  import * as vinculosApi from '../api/vinculos.api'
  import { mensagemDeErro } from '../api/http'
  import type { Esporte } from '../models/esporte.model'
  import type { AtletaEsporte } from '../models/vinculo.model'

  let disponiveis = $state<Esporte[]>([])
  let aprovados = $state<AtletaEsporte[]>([])
  let pendentes = $state<AtletaEsporte[]>([])
  let carregando = $state(true)
  let ocupadoId = $state('')
  let erro = $state('')
  let sucesso = $state('')

  // Esportes em que o atleta já está (ou já pediu) não podem ser pedidos de novo.
  const idsOcupados = $derived(new Set([...aprovados, ...pendentes].map((v) => v.esporte_id)))
  const podePedir = $derived(disponiveis.filter((e) => !idsOcupados.has(e.id)))

  async function carregar() {
    try {
      const [todos, ok, aguardando] = await Promise.all([
        vinculosApi.esportesDisponiveis(),
        vinculosApi.meusEsportes(),
        vinculosApi.minhasSolicitacoes(),
      ])
      disponiveis = todos
      aprovados = ok
      pendentes = aguardando
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  async function pedir(esporte: Esporte) {
    erro = ''
    sucesso = ''
    ocupadoId = esporte.id
    try {
      await vinculosApi.solicitar(esporte.id)
      sucesso = `Pedido enviado para "${esporte.nome}". Aguarde a decisão do treinador.`
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      ocupadoId = ''
    }
  }

  async function cancelar(vinculo: AtletaEsporte) {
    erro = ''
    sucesso = ''
    ocupadoId = vinculo.id
    try {
      await vinculosApi.cancelar(vinculo.id)
      sucesso = 'Pedido cancelado.'
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      ocupadoId = ''
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Meus esportes" subtitulo="Peça para entrar em um esporte e acompanhe a resposta do treinador." />

<div class="space-y-6">
  <Alert tipo="erro" mensagem={erro} />
  <Alert tipo="sucesso" mensagem={sucesso} />

  {#if carregando}
    <Loading />
  {:else}
    <Cartao titulo="Esportes em que participo">
      {#if aprovados.length === 0}
        <Vazio texto="Você ainda não participa de nenhum esporte." />
      {:else}
        <div class="flex flex-wrap gap-2">
          {#each aprovados as vinculo (vinculo.id)}
            <span class="rounded-full bg-emerald-100 px-4 py-1.5 text-sm font-semibold text-emerald-800">
              {vinculo.esporte_nome ?? 'Esporte'}
            </span>
          {/each}
        </div>
      {/if}
    </Cartao>

    {#if pendentes.length > 0}
      <Cartao titulo="Pedidos aguardando resposta">
        <ul class="divide-y divide-slate-100">
          {#each pendentes as vinculo (vinculo.id)}
            <li class="flex items-center justify-between gap-3 py-3">
              <div class="flex items-center gap-3">
                <span class="font-medium text-slate-900">{vinculo.esporte_nome ?? 'Esporte'}</span>
                <StatusBadge status={vinculo.status} />
              </div>
              <button
                class="btn-claro btn-pequeno"
                disabled={ocupadoId === vinculo.id}
                onclick={() => cancelar(vinculo)}
              >
                Cancelar pedido
              </button>
            </li>
          {/each}
        </ul>
      </Cartao>
    {/if}

    <Cartao titulo="Esportes disponíveis">
      {#if podePedir.length === 0}
        <Vazio texto="Não há outros esportes disponíveis no momento." />
      {:else}
        <div class="grid gap-3 sm:grid-cols-2">
          {#each podePedir as esporte (esporte.id)}
            <div class="flex items-start justify-between gap-3 rounded-xl border border-slate-200 p-4">
              <div>
                <p class="font-semibold text-slate-900">{esporte.nome}</p>
                {#if esporte.descricao}
                  <p class="mt-1 text-sm text-slate-500">{esporte.descricao}</p>
                {/if}
              </div>
              <button
                class="btn-primario btn-pequeno shrink-0"
                disabled={ocupadoId === esporte.id}
                onclick={() => pedir(esporte)}
              >
                Participar
              </button>
            </div>
          {/each}
        </div>
      {/if}
    </Cartao>
  {/if}
</div>
