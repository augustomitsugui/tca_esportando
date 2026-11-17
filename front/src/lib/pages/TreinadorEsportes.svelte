<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Campo from '../components/Campo.svelte'
  import Cartao from '../components/Cartao.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import Vazio from '../components/Vazio.svelte'
  import * as esportesApi from '../api/esportes.api'
  import { mensagemDeErro } from '../api/http'
  import type { Esporte } from '../models/esporte.model'
  import { textoOuNull } from '../utils/formatar'

  let esportes = $state<Esporte[]>([])
  let carregando = $state(true)
  let salvando = $state(false)
  let erro = $state('')
  let sucesso = $state('')

  // O mesmo formulário serve para criar e para editar
  let editandoId = $state('')
  let nome = $state('')
  let descricao = $state('')

  async function carregar() {
    try {
      esportes = await esportesApi.listarDoTreinador()
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

  function editar(esporte: Esporte) {
    editandoId = esporte.id
    nome = esporte.nome
    descricao = esporte.descricao ?? ''
    erro = ''
    sucesso = ''
  }

  async function salvar(evento: Event) {
    evento.preventDefault()
    erro = ''
    sucesso = ''
    salvando = true
    try {
      const dados = { nome: nome.trim(), descricao: textoOuNull(descricao) }
      if (editandoId) {
        await esportesApi.atualizar(editandoId, dados)
        sucesso = 'Esporte atualizado.'
      } else {
        await esportesApi.criar(dados)
        sucesso = 'Esporte criado.'
      }
      limparFormulario()
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      salvando = false
    }
  }

  async function excluir(esporte: Esporte) {
    if (!confirm(`Excluir o esporte "${esporte.nome}"?`)) return
    erro = ''
    sucesso = ''
    try {
      await esportesApi.excluir(esporte.id)
      sucesso = 'Esporte excluído.'
      if (editandoId === esporte.id) limparFormulario()
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Esportes" subtitulo="Os esportes que você administra na sua instituição." />

<div class="grid gap-6 lg:grid-cols-3">
  <div class="lg:col-span-1">
    <Cartao titulo={editandoId ? 'Editar esporte' : 'Novo esporte'}>
      <form class="space-y-4" onsubmit={salvar}>
        <Campo rotulo="Nome" bind:valor={nome} obrigatorio maxlength={100} />
        <label class="block">
          <span class="rotulo">Descrição</span>
          <textarea class="campo" rows="3" maxlength="1024" bind:value={descricao}></textarea>
        </label>
        <div class="flex gap-2">
          <button type="submit" class="btn-primario" disabled={salvando}>
            {salvando ? 'Salvando...' : editandoId ? 'Salvar' : 'Criar esporte'}
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
    {:else if esportes.length === 0}
      <Vazio texto="Você ainda não criou nenhum esporte." />
    {:else}
      <div class="grid gap-4 sm:grid-cols-2">
        {#each esportes as esporte (esporte.id)}
          <div class="cartao flex flex-col justify-between">
            <div>
              <h3 class="text-lg font-bold text-slate-900">{esporte.nome}</h3>
              <p class="mt-1 text-sm text-slate-500">{esporte.descricao ?? 'Sem descrição.'}</p>
            </div>
            <div class="mt-4 flex gap-2">
              <button class="btn-claro btn-pequeno" onclick={() => editar(esporte)}>Editar</button>
              <button class="btn-perigo btn-pequeno" onclick={() => excluir(esporte)}>Excluir</button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
