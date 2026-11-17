<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Cartao from '../components/Cartao.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import Vazio from '../components/Vazio.svelte'
  import * as treinosApi from '../api/treinos.api'
  import * as vinculosApi from '../api/vinculos.api'
  import { mensagemDeErro } from '../api/http'
  import type { TreinoAgenda } from '../models/treino.model'
  import { auth } from '../state/auth.svelte'
  import { router } from '../state/router.svelte'
  import { formatarDataHora } from '../utils/formatar'

  let proximos = $state<TreinoAgenda[]>([])
  let totalEsportes = $state(0)
  let totalPendentes = $state(0)
  let carregando = $state(true)
  let erro = $state('')

  async function carregar() {
    const atletaId = auth.usuario?.profile_id
    if (!atletaId) {
      erro = 'Perfil de atleta não encontrado para esta conta.'
      carregando = false
      return
    }
    try {
      const [agenda, aprovados, pendentes] = await Promise.all([
        treinosApi.proximosDoAtleta(atletaId),
        vinculosApi.meusEsportes(),
        vinculosApi.minhasSolicitacoes(),
      ])
      proximos = agenda
      totalEsportes = aprovados.length
      totalPendentes = pendentes.length
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Olá, atleta! 👋" subtitulo="Veja seus esportes e os próximos treinos." />

<div class="space-y-6">
  <Alert tipo="erro" mensagem={erro} />

  {#if carregando}
    <Loading />
  {:else}
    <div class="grid gap-4 sm:grid-cols-3">
      <div class="cartao">
        <p class="text-sm text-slate-500">Esportes aprovados</p>
        <p class="mt-1 text-3xl font-bold text-emerald-600">{totalEsportes}</p>
      </div>
      <div class="cartao">
        <p class="text-sm text-slate-500">Pedidos aguardando</p>
        <p class="mt-1 text-3xl font-bold text-amber-500">{totalPendentes}</p>
      </div>
      <div class="cartao">
        <p class="text-sm text-slate-500">Próximos treinos</p>
        <p class="mt-1 text-3xl font-bold text-sky-600">{proximos.length}</p>
      </div>
    </div>

    <Cartao titulo="Próximos treinos">
      {#if proximos.length === 0}
        <Vazio texto="Nenhum treino marcado. Peça para entrar em um esporte para ver os treinos." />
      {:else}
        <ul class="divide-y divide-slate-100">
          {#each proximos.slice(0, 5) as treino (treino.treino_id)}
            <li class="flex flex-wrap items-center justify-between gap-2 py-3">
              <div>
                <p class="font-semibold text-slate-900">{treino.treino_nome}</p>
                <p class="text-sm text-slate-500">
                  {treino.esporte_nome} · {treino.local_nome} · {treino.treinador_nome}
                </p>
              </div>
              <span class="rounded-full bg-sky-100 px-3 py-1 text-xs font-semibold text-sky-800">
                {formatarDataHora(treino.data_hora)}
              </span>
            </li>
          {/each}
        </ul>
      {/if}
    </Cartao>

    <div class="flex flex-wrap gap-3">
      <button class="btn-primario" onclick={() => router.navegar('esportes')}>Ver esportes</button>
      <button class="btn-claro" onclick={() => router.navegar('treinos')}>Ver todos os treinos</button>
    </div>
  {/if}
</div>
