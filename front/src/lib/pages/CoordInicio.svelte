<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Cartao from '../components/Cartao.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import * as esportesApi from '../api/esportes.api'
  import * as instituicoesApi from '../api/instituicoes.api'
  import * as locaisApi from '../api/locais.api'
  import * as solicitacoesApi from '../api/solicitacoes.api'
  import { mensagemDeErro } from '../api/http'
  import type { Instituicao } from '../models/instituicao.model'
  import { router } from '../state/router.svelte'

  let instituicao = $state<Instituicao | null>(null)
  let totalPendentes = $state(0)
  let totalLocais = $state(0)
  let totalEsportes = $state(0)
  let carregando = $state(true)
  let erro = $state('')

  async function carregar() {
    try {
      const [instituicoes, pendentes, locais, esportes] = await Promise.all([
        instituicoesApi.listar(),
        solicitacoesApi.pendentesDoCoordenador(),
        locaisApi.listar(),
        esportesApi.listarDoCoordenador(),
      ])
      instituicao = instituicoes[0] ?? null
      totalPendentes = pendentes.length
      totalLocais = locais.length
      totalEsportes = esportes.length
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Painel do coordenador 🏫" subtitulo="Cuide da sua instituição, locais e treinadores." />

<div class="space-y-6">
  <Alert tipo="erro" mensagem={erro} />

  {#if carregando}
    <Loading />
  {:else}
    {#if instituicao}
      <Cartao>
        <p class="text-sm text-slate-500">Sua instituição</p>
        <h2 class="text-xl font-bold text-slate-900">{instituicao.nome}</h2>
        {#if instituicao.descricao}
          <p class="mt-1 text-sm text-slate-600">{instituicao.descricao}</p>
        {/if}
      </Cartao>
    {/if}

    <div class="grid gap-4 sm:grid-cols-3">
      <div class="cartao">
        <p class="text-sm text-slate-500">Treinadores aguardando</p>
        <p class="mt-1 text-3xl font-bold text-amber-500">{totalPendentes}</p>
      </div>
      <div class="cartao">
        <p class="text-sm text-slate-500">Locais</p>
        <p class="mt-1 text-3xl font-bold text-sky-600">{totalLocais}</p>
      </div>
      <div class="cartao">
        <p class="text-sm text-slate-500">Esportes da instituição</p>
        <p class="mt-1 text-3xl font-bold text-emerald-600">{totalEsportes}</p>
      </div>
    </div>

    <div class="flex flex-wrap gap-3">
      <button class="btn-primario" onclick={() => router.navegar('solicitacoes')}>
        Ver solicitações {#if totalPendentes > 0}({totalPendentes}){/if}
      </button>
      <button class="btn-claro" onclick={() => router.navegar('locais')}>Gerenciar locais</button>
      <button class="btn-claro" onclick={() => router.navegar('instituicao')}>Minha instituição</button>
    </div>
  {/if}
</div>
