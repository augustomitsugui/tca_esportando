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
  import * as treinosApi from '../api/treinos.api'
  import { mensagemDeErro } from '../api/http'
  import type { Esporte } from '../models/esporte.model'
  import type { Local } from '../models/local.model'
  import type { Treino } from '../models/treino.model'
  import { auth } from '../state/auth.svelte'
  import { deInputLocal, formatarDataHora, paraInputLocal, textoOuNull } from '../utils/formatar'

  let treinos = $state<Treino[]>([])
  let esportes = $state<Esporte[]>([])
  let locais = $state<Local[]>([])
  let carregando = $state(true)
  let salvando = $state(false)
  let erro = $state('')
  let sucesso = $state('')

  let editandoId = $state('')
  let nome = $state('')
  let descricao = $state('')
  let dataHora = $state('')
  let esporteId = $state('')
  let localId = $state('')

  const faltaConfigurar = $derived(esportes.length === 0 || locais.length === 0)

  function nomeDoEsporte(id: string): string {
    return esportes.find((e) => e.id === id)?.nome ?? '—'
  }

  function nomeDoLocal(id: string): string {
    return locais.find((l) => l.id === id)?.nome ?? '—'
  }

  async function carregar() {
    try {
      const [listaTreinos, listaEsportes, listaLocais] = await Promise.all([
        treinosApi.listar(),
        esportesApi.listarDoTreinador(),
        locaisApi.listarDoTreinador(),
      ])
      treinos = listaTreinos
      esportes = listaEsportes
      locais = listaLocais
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
    dataHora = ''
    esporteId = ''
    localId = ''
  }

  function editar(treino: Treino) {
    editandoId = treino.id
    nome = treino.nome
    descricao = treino.descricao ?? ''
    dataHora = paraInputLocal(treino.data_hora)
    esporteId = treino.esporte_id
    localId = treino.local_id
    erro = ''
    sucesso = ''
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function salvar(evento: Event) {
    evento.preventDefault()
    erro = ''
    sucesso = ''

    const treinadorId = auth.usuario?.profile_id
    if (!treinadorId) {
      erro = 'Perfil de treinador não encontrado para esta conta.'
      return
    }

    salvando = true
    try {
      // Sempre enviamos todos os campos (o backend trata campo ausente como "apagar").
      const dados = {
        nome: nome.trim(),
        descricao: textoOuNull(descricao),
        data_hora: deInputLocal(dataHora),
        treinador_id: treinadorId,
        local_id: localId,
        esporte_id: esporteId,
      }
      if (editandoId) {
        await treinosApi.atualizar(editandoId, dados)
        sucesso = 'Treino atualizado.'
      } else {
        await treinosApi.criar(dados)
        sucesso = 'Treino criado.'
      }
      limparFormulario()
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      salvando = false
    }
  }

  async function excluir(treino: Treino) {
    if (!confirm(`Excluir o treino "${treino.nome}"?`)) return
    erro = ''
    sucesso = ''
    try {
      await treinosApi.excluir(treino.id)
      sucesso = 'Treino excluído.'
      if (editandoId === treino.id) limparFormulario()
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Treinos" subtitulo="Crie e organize os treinos dos seus esportes." />

<div class="space-y-6">
  <Alert tipo="erro" mensagem={erro} />
  <Alert tipo="sucesso" mensagem={sucesso} />

  {#if carregando}
    <Loading />
  {:else}
    {#if faltaConfigurar}
      <Alert
        tipo="info"
        mensagem="Para criar um treino você precisa ter pelo menos um esporte e um local. Os locais aparecem aqui quando o coordenador os vincula à sua instituição."
      />
    {/if}

    <Cartao titulo={editandoId ? 'Editar treino' : 'Novo treino'}>
      <form class="space-y-4" onsubmit={salvar}>
        <div class="grid gap-4 sm:grid-cols-2">
          <Campo rotulo="Nome do treino" bind:valor={nome} obrigatorio maxlength={100} />
          <Campo rotulo="Data e hora" tipo="datetime-local" bind:valor={dataHora} obrigatorio />

          <label class="block">
            <span class="rotulo">Esporte <span class="text-red-500">*</span></span>
            <select class="campo" bind:value={esporteId} required>
              <option value="" disabled>Selecione</option>
              {#each esportes as esporte (esporte.id)}
                <option value={esporte.id}>{esporte.nome}</option>
              {/each}
            </select>
          </label>

          <label class="block">
            <span class="rotulo">Local <span class="text-red-500">*</span></span>
            <select class="campo" bind:value={localId} required>
              <option value="" disabled>Selecione</option>
              {#each locais as local (local.id)}
                <option value={local.id}>{local.nome}</option>
              {/each}
            </select>
          </label>
        </div>

        <label class="block">
          <span class="rotulo">Descrição</span>
          <textarea class="campo" rows="2" maxlength="1024" bind:value={descricao}></textarea>
        </label>

        <div class="flex gap-2">
          <button type="submit" class="btn-primario" disabled={salvando || faltaConfigurar}>
            {salvando ? 'Salvando...' : editandoId ? 'Salvar alterações' : 'Criar treino'}
          </button>
          {#if editandoId}
            <button type="button" class="btn-claro" onclick={limparFormulario}>Cancelar</button>
          {/if}
        </div>
      </form>
    </Cartao>

    <Cartao titulo="Treinos cadastrados">
      {#if treinos.length === 0}
        <Vazio texto="Nenhum treino cadastrado ainda." />
      {:else}
        <div class="-mx-5 overflow-x-auto sm:-mx-6">
          <table class="tabela">
            <thead>
              <tr>
                <th>Treino</th>
                <th>Esporte</th>
                <th>Local</th>
                <th>Data e hora</th>
                <th class="text-right">Ações</th>
              </tr>
            </thead>
            <tbody>
              {#each treinos as treino (treino.id)}
                <tr>
                  <td>
                    <p class="font-medium text-slate-900">{treino.nome}</p>
                    {#if treino.descricao}
                      <p class="text-xs text-slate-500">{treino.descricao}</p>
                    {/if}
                  </td>
                  <td>{nomeDoEsporte(treino.esporte_id)}</td>
                  <td>{nomeDoLocal(treino.local_id)}</td>
                  <td class="whitespace-nowrap">{formatarDataHora(treino.data_hora)}</td>
                  <td>
                    <div class="flex justify-end gap-2">
                      <button class="btn-claro btn-pequeno" onclick={() => editar(treino)}>Editar</button>
                      <button class="btn-perigo btn-pequeno" onclick={() => excluir(treino)}>Excluir</button>
                    </div>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </Cartao>
  {/if}
</div>
