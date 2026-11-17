<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Campo from '../components/Campo.svelte'
  import Cartao from '../components/Cartao.svelte'
  import Loading from '../components/Loading.svelte'
  import StatusBadge from '../components/StatusBadge.svelte'
  import Titulo from '../components/Titulo.svelte'
  import * as instituicoesApi from '../api/instituicoes.api'
  import * as solicitacoesApi from '../api/solicitacoes.api'
  import { mensagemDeErro } from '../api/http'
  import type { InstituicaoPublica } from '../models/instituicao.model'
  import type { RoleRequest } from '../models/solicitacao.model'
  import { auth } from '../state/auth.svelte'
  import { formatarDataHora, numeroOuNull, textoOuNull } from '../utils/formatar'

  // Tela do treinador/coordenador que ainda NÃO foi aprovado (ou foi recusado).
  // O backend só libera /auth/me e /role-requests/me para quem está nesse estado.

  let ultima = $state<RoleRequest | null>(null)
  let instituicoes = $state<InstituicaoPublica[]>([])
  let carregando = $state(true)
  let atualizando = $state(false)
  let erro = $state('')
  let sucesso = $state('')

  // Formulário de nova solicitação (só aparece se a anterior foi recusada)
  let instituicaoId = $state('')
  let nomeInstituicao = $state('')
  let descricaoInstituicao = $state('')
  let latitude = $state('')
  let longitude = $state('')
  let enviando = $state(false)

  const papel = $derived(auth.usuario?.role === 'coordenador' ? 'coordenador' : 'treinador')
  const quemAprova = $derived(
    papel === 'coordenador' ? 'o administrador do sistema' : 'o coordenador da sua instituição',
  )
  const nomeInstituicaoDoPedido = $derived(
    ultima?.institution_name ??
      instituicoes.find((i) => i.id === ultima?.institution_id)?.nome ??
      '—',
  )

  async function carregar() {
    erro = ''
    try {
      const lista = await solicitacoesApi.minhas()
      ultima =
        [...lista].sort((a, b) => b.created_at.localeCompare(a.created_at))[0] ?? null
      if (papel === 'treinador') {
        instituicoes = await instituicoesApi.listarPublicas()
      }
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  async function atualizarSituacao() {
    atualizando = true
    erro = ''
    sucesso = ''
    try {
      await auth.atualizar() // se foi aprovado, o perfil muda e o dashboard aparece sozinho
      await carregar()
      sucesso = 'Situação atualizada.'
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      atualizando = false
    }
  }

  async function enviarNova(evento: Event) {
    evento.preventDefault()
    erro = ''
    sucesso = ''
    enviando = true
    try {
      if (papel === 'treinador') {
        if (instituicaoId === '') {
          erro = 'Escolha a instituição.'
          return
        }
        await solicitacoesApi.enviarNova({ requested_role: 'treinador', institution_id: instituicaoId })
      } else {
        await solicitacoesApi.enviarNova({
          requested_role: 'coordenador',
          institution_name: nomeInstituicao.trim(),
          institution_description: textoOuNull(descricaoInstituicao),
          institution_latitude: numeroOuNull(latitude),
          institution_longitude: numeroOuNull(longitude),
        })
      }
      await auth.atualizar()
      await carregar()
      sucesso = 'Nova solicitação enviada.'
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      enviando = false
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Minha solicitação" subtitulo="Acompanhe a aprovação do seu cadastro.">
  <button class="btn-claro" onclick={atualizarSituacao} disabled={atualizando}>
    {atualizando ? 'Atualizando...' : 'Atualizar situação'}
  </button>
</Titulo>

<div class="space-y-4">
  <Alert tipo="erro" mensagem={erro} />
  <Alert tipo="sucesso" mensagem={sucesso} />

  {#if carregando}
    <Loading />
  {:else if ultima}
    <Cartao>
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm text-slate-500">Cargo solicitado</p>
          <p class="text-lg font-semibold capitalize text-slate-900">{ultima.requested_role}</p>
        </div>
        <StatusBadge status={ultima.status} />
      </div>

      <dl class="mt-4 grid gap-3 text-sm sm:grid-cols-2">
        <div>
          <dt class="text-slate-500">Instituição</dt>
          <dd class="font-medium text-slate-900">{nomeInstituicaoDoPedido}</dd>
        </div>
        <div>
          <dt class="text-slate-500">Enviada em</dt>
          <dd class="font-medium text-slate-900">{formatarDataHora(ultima.created_at)}</dd>
        </div>
        {#if ultima.decided_at}
          <div>
            <dt class="text-slate-500">Decidida em</dt>
            <dd class="font-medium text-slate-900">{formatarDataHora(ultima.decided_at)}</dd>
          </div>
        {/if}
      </dl>

      {#if ultima.status === 'pendente'}
        <div class="mt-5">
          <Alert
            tipo="info"
            mensagem={`Seu pedido está aguardando ${quemAprova}. Quando for aprovado, clique em "Atualizar situação" para liberar o seu painel.`}
          />
        </div>
      {:else if ultima.status === 'rejeitada'}
        <div class="mt-5 space-y-3">
          <Alert
            tipo="erro"
            mensagem={`Seu pedido foi recusado. Motivo: ${ultima.rejection_reason ?? 'não informado'}.`}
          />
        </div>
      {/if}
    </Cartao>

    {#if ultima.status === 'rejeitada'}
      <Cartao titulo="Enviar uma nova solicitação">
        <form class="space-y-4" onsubmit={enviarNova}>
          {#if papel === 'treinador'}
            <label class="block">
              <span class="rotulo">Instituição</span>
              <select class="campo" bind:value={instituicaoId} required>
                <option value="" disabled>Selecione a instituição</option>
                {#each instituicoes as instituicao (instituicao.id)}
                  <option value={instituicao.id}>{instituicao.nome}</option>
                {/each}
              </select>
            </label>
          {:else}
            <Campo rotulo="Nome da instituição" bind:valor={nomeInstituicao} obrigatorio maxlength={100} />
            <label class="block">
              <span class="rotulo">Descrição</span>
              <textarea class="campo" rows="2" maxlength="1024" bind:value={descricaoInstituicao}></textarea>
            </label>
            <div class="grid gap-4 sm:grid-cols-2">
              <Campo rotulo="Latitude (opcional)" bind:valor={latitude} />
              <Campo rotulo="Longitude (opcional)" bind:valor={longitude} />
            </div>
          {/if}
          <button type="submit" class="btn-primario" disabled={enviando}>
            {enviando ? 'Enviando...' : 'Enviar nova solicitação'}
          </button>
        </form>
      </Cartao>
    {/if}
  {:else}
    <Alert tipo="info" mensagem="Nenhuma solicitação encontrada para a sua conta." />
  {/if}
</div>
