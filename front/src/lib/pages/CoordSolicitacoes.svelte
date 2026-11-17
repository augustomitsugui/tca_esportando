<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import ListaSolicitacoes from '../components/ListaSolicitacoes.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import * as solicitacoesApi from '../api/solicitacoes.api'
  import { mensagemDeErro } from '../api/http'
  import type { RoleRequest } from '../models/solicitacao.model'

  // O coordenador decide apenas os treinadores da PRÓPRIA instituição
  // (o backend também confere isso).

  let aba = $state<'pendentes' | 'historico'>('pendentes')
  let pendentes = $state<RoleRequest[]>([])
  let historico = $state<RoleRequest[]>([])
  let carregando = $state(true)
  let erro = $state('')
  let sucesso = $state('')

  async function carregar() {
    try {
      const [aguardando, todas] = await Promise.all([
        solicitacoesApi.pendentesDoCoordenador(),
        solicitacoesApi.historicoDoCoordenador(),
      ])
      pendentes = aguardando
      // O histórico mostra só o que já foi decidido
      historico = todas.filter((s) => s.status !== 'pendente')
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  async function aprovar(id: string) {
    erro = ''
    sucesso = ''
    try {
      await solicitacoesApi.aprovar(id)
      sucesso = 'Treinador aprovado.'
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    }
  }

  async function rejeitar(id: string, motivo: string) {
    erro = ''
    sucesso = ''
    try {
      await solicitacoesApi.rejeitar(id, motivo)
      sucesso = 'Solicitação recusada.'
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
      throw e // mantém o campo do motivo aberto
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Solicitações de treinadores" subtitulo="Aprove ou recuse quem quer treinar na sua instituição." />

<div class="space-y-4">
  <Alert tipo="erro" mensagem={erro} />
  <Alert tipo="sucesso" mensagem={sucesso} />

  <div class="inline-flex rounded-lg border border-slate-200 bg-white p-1">
    <button
      class="rounded-md px-4 py-1.5 text-sm font-semibold {aba === 'pendentes'
        ? 'bg-emerald-600 text-white'
        : 'text-slate-600'}"
      onclick={() => (aba = 'pendentes')}
    >
      Pendentes ({pendentes.length})
    </button>
    <button
      class="rounded-md px-4 py-1.5 text-sm font-semibold {aba === 'historico'
        ? 'bg-emerald-600 text-white'
        : 'text-slate-600'}"
      onclick={() => (aba = 'historico')}
    >
      Histórico
    </button>
  </div>

  {#if carregando}
    <Loading />
  {:else if aba === 'pendentes'}
    <ListaSolicitacoes
      itens={pendentes}
      textoVazio="Nenhum treinador aguardando aprovação."
      aoAprovar={aprovar}
      aoRejeitar={rejeitar}
    />
  {:else}
    <ListaSolicitacoes
      itens={historico}
      podeDecidir={false}
      textoVazio="Nenhuma solicitação decidida ainda."
      aoAprovar={aprovar}
      aoRejeitar={rejeitar}
    />
  {/if}
</div>
