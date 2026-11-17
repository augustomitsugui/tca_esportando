<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import ListaSolicitacoes from '../components/ListaSolicitacoes.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import * as solicitacoesApi from '../api/solicitacoes.api'
  import { mensagemDeErro } from '../api/http'
  import type { RoleRequest } from '../models/solicitacao.model'

  let pedidos = $state<RoleRequest[]>([])
  let carregando = $state(true)
  let erro = $state('')
  let sucesso = $state('')

  async function carregar() {
    try {
      const todas = await solicitacoesApi.pendentesDoAdmin()
      // O backend também lista pedidos de treinador, mas quem decide esses é o
      // coordenador da instituição. O ADMIN só decide coordenadores.
      pedidos = todas.filter((s) => s.requested_role === 'coordenador')
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
      sucesso = 'Coordenador aprovado e instituição criada.'
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
      throw e
    }
  }

  onMount(carregar)
</script>

<Titulo
  titulo="Solicitações de coordenadores"
  subtitulo="Ao aprovar, a instituição pedida é criada e o coordenador é liberado."
/>

<div class="space-y-4">
  <Alert tipo="erro" mensagem={erro} />
  <Alert tipo="sucesso" mensagem={sucesso} />

  {#if carregando}
    <Loading />
  {:else}
    <ListaSolicitacoes
      itens={pedidos}
      textoVazio="Nenhum coordenador aguardando aprovação."
      aoAprovar={aprovar}
      aoRejeitar={rejeitar}
    />
  {/if}
</div>
