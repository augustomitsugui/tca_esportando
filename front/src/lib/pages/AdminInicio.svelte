<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import * as instituicoesApi from '../api/instituicoes.api'
  import * as solicitacoesApi from '../api/solicitacoes.api'
  import { mensagemDeErro } from '../api/http'
  import { router } from '../state/router.svelte'

  let totalPendentes = $state(0)
  let totalInstituicoes = $state(0)
  let carregando = $state(true)
  let erro = $state('')

  async function carregar() {
    try {
      const [pedidos, instituicoes] = await Promise.all([
        solicitacoesApi.pendentesDoAdmin(),
        instituicoesApi.listar(),
      ])
      totalPendentes = pedidos.filter((p) => p.requested_role === 'coordenador').length
      totalInstituicoes = instituicoes.length
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Painel do administrador 🛠️" subtitulo="Aprove coordenadores e acompanhe as instituições." />

<div class="space-y-6">
  <Alert tipo="erro" mensagem={erro} />

  {#if carregando}
    <Loading />
  {:else}
    <div class="grid gap-4 sm:grid-cols-2">
      <div class="cartao">
        <p class="text-sm text-slate-500">Coordenadores aguardando aprovação</p>
        <p class="mt-1 text-3xl font-bold text-amber-500">{totalPendentes}</p>
      </div>
      <div class="cartao">
        <p class="text-sm text-slate-500">Instituições cadastradas</p>
        <p class="mt-1 text-3xl font-bold text-emerald-600">{totalInstituicoes}</p>
      </div>
    </div>

    <div class="flex flex-wrap gap-3">
      <button class="btn-primario" onclick={() => router.navegar('solicitacoes')}>
        Ver solicitações {#if totalPendentes > 0}({totalPendentes}){/if}
      </button>
      <button class="btn-claro" onclick={() => router.navegar('instituicoes')}>Ver instituições</button>
    </div>
  {/if}
</div>
