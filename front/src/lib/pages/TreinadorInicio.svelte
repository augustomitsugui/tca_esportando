<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import * as esportesApi from '../api/esportes.api'
  import * as treinosApi from '../api/treinos.api'
  import * as vinculosApi from '../api/vinculos.api'
  import { mensagemDeErro } from '../api/http'
  import { router } from '../state/router.svelte'

  let totalEsportes = $state(0)
  let totalTreinos = $state(0)
  let totalPedidos = $state(0)
  let totalAtletas = $state(0)
  let carregando = $state(true)
  let erro = $state('')

  async function carregar() {
    try {
      const [esportes, treinos, pedidos, atletas] = await Promise.all([
        esportesApi.listarDoTreinador(),
        treinosApi.listar(),
        vinculosApi.pendentesDoTreinador(),
        vinculosApi.atletasDoTreinador(),
      ])
      totalEsportes = esportes.length
      totalTreinos = treinos.length
      totalPedidos = pedidos.length
      totalAtletas = atletas.length
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Painel do treinador 🏅" subtitulo="Resumo dos seus esportes, treinos e atletas." />

<div class="space-y-6">
  <Alert tipo="erro" mensagem={erro} />

  {#if carregando}
    <Loading />
  {:else}
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div class="cartao">
        <p class="text-sm text-slate-500">Esportes</p>
        <p class="mt-1 text-3xl font-bold text-emerald-600">{totalEsportes}</p>
      </div>
      <div class="cartao">
        <p class="text-sm text-slate-500">Treinos</p>
        <p class="mt-1 text-3xl font-bold text-sky-600">{totalTreinos}</p>
      </div>
      <div class="cartao">
        <p class="text-sm text-slate-500">Pedidos de atletas</p>
        <p class="mt-1 text-3xl font-bold text-amber-500">{totalPedidos}</p>
      </div>
      <div class="cartao">
        <p class="text-sm text-slate-500">Atletas vinculados</p>
        <p class="mt-1 text-3xl font-bold text-slate-800">{totalAtletas}</p>
      </div>
    </div>

    <div class="flex flex-wrap gap-3">
      <button class="btn-primario" onclick={() => router.navegar('treinos')}>Gerenciar treinos</button>
      <button class="btn-claro" onclick={() => router.navegar('esportes')}>Meus esportes</button>
      <button class="btn-claro" onclick={() => router.navegar('atletas')}>
        Pedidos de atletas {#if totalPedidos > 0}({totalPedidos}){/if}
      </button>
    </div>
  {/if}
</div>
