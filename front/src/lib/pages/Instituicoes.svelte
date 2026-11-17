<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Campo from '../components/Campo.svelte'
  import Cartao from '../components/Cartao.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import Vazio from '../components/Vazio.svelte'
  import * as instituicoesApi from '../api/instituicoes.api'
  import { mensagemDeErro } from '../api/http'
  import type { Instituicao } from '../models/instituicao.model'
  import { auth } from '../state/auth.svelte'
  import { numeroOuNull, textoOuNull } from '../utils/formatar'

  // Usada pelo coordenador (só a própria instituição) e pelo ADMIN (todas).
  const ehAdmin = $derived(auth.perfil === 'admin')

  let instituicoes = $state<Instituicao[]>([])
  let carregando = $state(true)
  let salvando = $state(false)
  let erro = $state('')
  let sucesso = $state('')

  let editandoId = $state('')
  let nome = $state('')
  let descricao = $state('')
  let latitude = $state('')
  let longitude = $state('')

  async function carregar() {
    try {
      instituicoes = await instituicoesApi.listar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  function editar(instituicao: Instituicao) {
    editandoId = instituicao.id
    nome = instituicao.nome
    descricao = instituicao.descricao ?? ''
    latitude = instituicao.latitude === null ? '' : String(instituicao.latitude)
    longitude = instituicao.longitude === null ? '' : String(instituicao.longitude)
    erro = ''
    sucesso = ''
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function cancelar() {
    editandoId = ''
    nome = ''
    descricao = ''
    latitude = ''
    longitude = ''
  }

  async function salvar(evento: Event) {
    evento.preventDefault()
    erro = ''
    sucesso = ''
    salvando = true
    try {
      await instituicoesApi.atualizar(editandoId, {
        nome: nome.trim(),
        descricao: textoOuNull(descricao),
        latitude: numeroOuNull(latitude),
        longitude: numeroOuNull(longitude),
      })
      sucesso = 'Instituição atualizada.'
      cancelar()
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      salvando = false
    }
  }

  async function excluir(instituicao: Instituicao) {
    if (!confirm(`Excluir a instituição "${instituicao.nome}"? Esta ação não pode ser desfeita.`)) return
    erro = ''
    sucesso = ''
    try {
      await instituicoesApi.excluir(instituicao.id)
      sucesso = 'Instituição excluída.'
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    }
  }

  onMount(carregar)
</script>

<Titulo
  titulo={ehAdmin ? 'Instituições' : 'Minha instituição'}
  subtitulo={ehAdmin ? 'Todas as instituições do sistema.' : 'Dados da instituição que você coordena.'}
/>

<div class="space-y-6">
  <Alert tipo="erro" mensagem={erro} />
  <Alert tipo="sucesso" mensagem={sucesso} />

  {#if editandoId}
    <Cartao titulo="Editar instituição">
      <form class="space-y-4" onsubmit={salvar}>
        <Campo rotulo="Nome" bind:valor={nome} obrigatorio maxlength={100} />
        <label class="block">
          <span class="rotulo">Descrição</span>
          <textarea class="campo" rows="3" maxlength="1024" bind:value={descricao}></textarea>
        </label>
        <div class="grid gap-4 sm:grid-cols-2">
          <Campo rotulo="Latitude" bind:valor={latitude} placeholder="-25.5163" />
          <Campo rotulo="Longitude" bind:valor={longitude} placeholder="-48.5225" />
        </div>
        <div class="flex gap-2">
          <button type="submit" class="btn-primario" disabled={salvando}>
            {salvando ? 'Salvando...' : 'Salvar'}
          </button>
          <button type="button" class="btn-claro" onclick={cancelar}>Cancelar</button>
        </div>
      </form>
    </Cartao>
  {/if}

  {#if carregando}
    <Loading />
  {:else if instituicoes.length === 0}
    <Vazio texto="Nenhuma instituição encontrada." />
  {:else}
    <div class="grid gap-4 sm:grid-cols-2">
      {#each instituicoes as instituicao (instituicao.id)}
        <div class="cartao flex flex-col justify-between">
          <div>
            <h3 class="text-lg font-bold text-slate-900">{instituicao.nome}</h3>
            <p class="mt-1 text-sm text-slate-500">{instituicao.descricao ?? 'Sem descrição.'}</p>
            {#if instituicao.latitude !== null && instituicao.longitude !== null}
              <a
                class="mt-2 inline-block text-sm font-medium text-emerald-700 hover:underline"
                href="https://www.openstreetmap.org/?mlat={instituicao.latitude}&mlon={instituicao.longitude}#map=16/{instituicao.latitude}/{instituicao.longitude}"
                target="_blank"
                rel="noopener noreferrer"
              >
                📍 Ver no mapa
              </a>
            {/if}
          </div>
          <div class="mt-4 flex gap-2">
            <button class="btn-claro btn-pequeno" onclick={() => editar(instituicao)}>Editar</button>
            {#if ehAdmin}
              <button class="btn-perigo btn-pequeno" onclick={() => excluir(instituicao)}>Excluir</button>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
