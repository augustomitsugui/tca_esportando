<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Campo from '../components/Campo.svelte'
  import Cartao from '../components/Cartao.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import Vazio from '../components/Vazio.svelte'
  import * as esportesApi from '../api/esportes.api'
  import * as locaisApi from '../api/locais.api'
  import { mensagemDeErro } from '../api/http'
  import type { Esporte } from '../models/esporte.model'
  import type { Local } from '../models/local.model'
  import { auth } from '../state/auth.svelte'
  import { textoOuNull } from '../utils/formatar'

  // O coordenador cria locais e define:
  //  1) se o local pertence à instituição dele (necessário para o treinador usar o local);
  //  2) em quais esportes da instituição o local pode ser usado.

  interface Detalhe {
    naInstituicao: boolean
    esportesIds: string[]
  }

  const instituicaoId = $derived(auth.usuario?.institution_id ?? '')

  let locais = $state<Local[]>([])
  let esportes = $state<Esporte[]>([])
  let detalhes = $state<Record<string, Detalhe>>({})
  let carregando = $state(true)
  let salvando = $state(false)
  let ocupadoId = $state('')
  let erro = $state('')
  let sucesso = $state('')

  let editandoId = $state('')
  let nome = $state('')
  let descricao = $state('')

  async function carregar() {
    try {
      const [listaLocais, listaEsportes] = await Promise.all([
        locaisApi.listar(),
        esportesApi.listarDoCoordenador(),
      ])
      const lista = await Promise.all(
        listaLocais.map(async (local) => {
          const [vinculosInstituicao, esportesDoLocal] = await Promise.all([
            locaisApi.listarInstituicoes(local.id),
            locaisApi.listarEsportes(local.id),
          ])
          const detalhe: Detalhe = {
            naInstituicao: vinculosInstituicao.some((v) => v.instituicao_id === instituicaoId),
            esportesIds: esportesDoLocal.map((e) => e.id),
          }
          return [local.id, detalhe] as const
        }),
      )
      locais = listaLocais
      esportes = listaEsportes
      detalhes = Object.fromEntries(lista)
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  function limparFormulario() {
    editandoId = ''
    nome = ''
    descricao = ''
  }

  function editar(local: Local) {
    editandoId = local.id
    nome = local.nome
    descricao = local.descricao ?? ''
    erro = ''
    sucesso = ''
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function salvar(evento: Event) {
    evento.preventDefault()
    erro = ''
    sucesso = ''
    salvando = true
    try {
      const dados = { nome: nome.trim(), descricao: textoOuNull(descricao) }
      if (editandoId) {
        await locaisApi.atualizar(editandoId, dados)
        sucesso = 'Local atualizado.'
      } else {
        const novo = await locaisApi.criar(dados)
        // Já vincula à instituição para o treinador conseguir usar o local.
        if (instituicaoId) await locaisApi.vincularInstituicao(novo.id, instituicaoId)
        sucesso = 'Local criado e vinculado à sua instituição.'
      }
      limparFormulario()
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      salvando = false
    }
  }

  async function excluir(local: Local) {
    if (!confirm(`Excluir o local "${local.nome}"?`)) return
    erro = ''
    sucesso = ''
    try {
      await locaisApi.excluir(local.id)
      sucesso = 'Local excluído.'
      if (editandoId === local.id) limparFormulario()
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    }
  }

  async function alternarInstituicao(local: Local) {
    erro = ''
    sucesso = ''
    ocupadoId = local.id
    try {
      if (detalhes[local.id]?.naInstituicao) {
        await locaisApi.desvincularInstituicao(local.id, instituicaoId)
      } else {
        await locaisApi.vincularInstituicao(local.id, instituicaoId)
      }
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      ocupadoId = ''
    }
  }

  async function alternarEsporte(local: Local, esporte: Esporte) {
    erro = ''
    sucesso = ''
    ocupadoId = local.id + esporte.id
    try {
      if (detalhes[local.id]?.esportesIds.includes(esporte.id)) {
        await locaisApi.desvincularEsporte(local.id, esporte.id)
      } else {
        await locaisApi.vincularEsporte(local.id, esporte.id)
      }
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      ocupadoId = ''
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Locais" subtitulo="Quadras, ginásios e campos usados nos treinos." />

<div class="grid gap-6 lg:grid-cols-3">
  <div class="lg:col-span-1">
    <Cartao titulo={editandoId ? 'Editar local' : 'Novo local'}>
      <form class="space-y-4" onsubmit={salvar}>
        <Campo rotulo="Nome" bind:valor={nome} obrigatorio maxlength={100} />
        <label class="block">
          <span class="rotulo">Descrição</span>
          <textarea class="campo" rows="3" maxlength="1024" bind:value={descricao}></textarea>
        </label>
        <div class="flex gap-2">
          <button type="submit" class="btn-primario" disabled={salvando}>
            {salvando ? 'Salvando...' : editandoId ? 'Salvar' : 'Criar local'}
          </button>
          {#if editandoId}
            <button type="button" class="btn-claro" onclick={limparFormulario}>Cancelar</button>
          {/if}
        </div>
      </form>
    </Cartao>
  </div>

  <div class="space-y-4 lg:col-span-2">
    <Alert tipo="erro" mensagem={erro} />
    <Alert tipo="sucesso" mensagem={sucesso} />

    {#if carregando}
      <Loading />
    {:else if locais.length === 0}
      <Vazio texto="Nenhum local cadastrado ainda." />
    {:else}
      {#each locais as local (local.id)}
        {@const detalhe = detalhes[local.id]}
        <div class="cartao">
          <div class="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h3 class="text-lg font-bold text-slate-900">{local.nome}</h3>
              <p class="text-sm text-slate-500">{local.descricao ?? 'Sem descrição.'}</p>
            </div>
            <div class="flex gap-2">
              <button class="btn-claro btn-pequeno" onclick={() => editar(local)}>Editar</button>
              <button class="btn-perigo btn-pequeno" onclick={() => excluir(local)}>Excluir</button>
            </div>
          </div>

          <div class="mt-4 space-y-3 border-t border-slate-100 pt-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <p class="text-sm text-slate-700">
                {#if detalhe?.naInstituicao}
                  ✅ Disponível para os treinadores da sua instituição
                {:else}
                  ⚠️ Fora da sua instituição: os treinadores não conseguem usar este local
                {/if}
              </p>
              <button
                class="btn-claro btn-pequeno"
                disabled={ocupadoId === local.id || !instituicaoId}
                onclick={() => alternarInstituicao(local)}
              >
                {detalhe?.naInstituicao ? 'Remover da instituição' : 'Vincular à instituição'}
              </button>
            </div>

            <div>
              <p class="mb-2 text-sm font-medium text-slate-700">Esportes praticados neste local</p>
              {#if esportes.length === 0}
                <p class="text-sm text-slate-500">
                  Ainda não há esportes na sua instituição (eles são criados pelos treinadores).
                </p>
              {:else}
                <div class="flex flex-wrap gap-2">
                  {#each esportes as esporte (esporte.id)}
                    {@const marcado = detalhe?.esportesIds.includes(esporte.id) ?? false}
                    <button
                      class="rounded-full border px-3 py-1 text-xs font-semibold transition disabled:opacity-50 {marcado
                        ? 'border-emerald-600 bg-emerald-600 text-white'
                        : 'border-slate-300 bg-white text-slate-600 hover:bg-slate-50'}"
                      disabled={ocupadoId === local.id + esporte.id}
                      onclick={() => alternarEsporte(local, esporte)}
                    >
                      {marcado ? '✓ ' : ''}{esporte.nome}
                    </button>
                  {/each}
                </div>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    {/if}
  </div>
</div>
