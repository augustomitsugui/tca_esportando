<script lang="ts">
  import { onMount } from 'svelte'
  import Alert from '../components/Alert.svelte'
  import Cartao from '../components/Cartao.svelte'
  import Loading from '../components/Loading.svelte'
  import Titulo from '../components/Titulo.svelte'
  import Vazio from '../components/Vazio.svelte'
  import * as vinculosApi from '../api/vinculos.api'
  import { mensagemDeErro } from '../api/http'
  import type { AtletaEsporte } from '../models/vinculo.model'

  let pedidos = $state<AtletaEsporte[]>([])
  let atletas = $state<AtletaEsporte[]>([])
  let carregando = $state(true)
  let ocupadoId = $state('')
  let erro = $state('')
  let sucesso = $state('')

  async function carregar() {
    try {
      const [listaPedidos, listaAtletas] = await Promise.all([
        vinculosApi.pendentesDoTreinador(),
        vinculosApi.atletasDoTreinador(),
      ])
      pedidos = listaPedidos
      atletas = listaAtletas
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      carregando = false
    }
  }

  async function decidir(pedido: AtletaEsporte, status: 'aprovado' | 'recusado') {
    erro = ''
    sucesso = ''
    ocupadoId = pedido.id
    try {
      await vinculosApi.decidir(pedido.id, status)
      sucesso = status === 'aprovado' ? 'Atleta aprovado.' : 'Pedido recusado.'
      await carregar()
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      ocupadoId = ''
    }
  }

  onMount(carregar)
</script>

<Titulo titulo="Atletas" subtitulo="Aprove quem quer participar dos seus esportes." />

<div class="space-y-6">
  <Alert tipo="erro" mensagem={erro} />
  <Alert tipo="sucesso" mensagem={sucesso} />

  {#if carregando}
    <Loading />
  {:else}
    <Cartao titulo="Pedidos para participar ({pedidos.length})">
      {#if pedidos.length === 0}
        <Vazio texto="Nenhum pedido pendente." />
      {:else}
        <ul class="divide-y divide-slate-100">
          {#each pedidos as pedido (pedido.id)}
            <li class="flex flex-wrap items-center justify-between gap-3 py-3">
              <div>
                <p class="font-semibold text-slate-900">{pedido.atleta_nome ?? 'Atleta'}</p>
                <p class="text-sm text-slate-500">quer participar de {pedido.esporte_nome ?? 'esporte'}</p>
              </div>
              <div class="flex gap-2">
                <button
                  class="btn-primario btn-pequeno"
                  disabled={ocupadoId === pedido.id}
                  onclick={() => decidir(pedido, 'aprovado')}
                >
                  Aprovar
                </button>
                <button
                  class="btn-perigo btn-pequeno"
                  disabled={ocupadoId === pedido.id}
                  onclick={() => decidir(pedido, 'recusado')}
                >
                  Recusar
                </button>
              </div>
            </li>
          {/each}
        </ul>
      {/if}
    </Cartao>

    <Cartao titulo="Atletas vinculados ({atletas.length})">
      {#if atletas.length === 0}
        <Vazio texto="Nenhum atleta aprovado nos seus esportes ainda." />
      {:else}
        <div class="-mx-5 overflow-x-auto sm:-mx-6">
          <table class="tabela">
            <thead>
              <tr>
                <th>Atleta</th>
                <th>Esporte</th>
              </tr>
            </thead>
            <tbody>
              {#each atletas as vinculo (vinculo.id)}
                <tr>
                  <td class="font-medium text-slate-900">{vinculo.atleta_nome ?? '—'}</td>
                  <td>{vinculo.esporte_nome ?? '—'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </Cartao>
  {/if}
</div>
