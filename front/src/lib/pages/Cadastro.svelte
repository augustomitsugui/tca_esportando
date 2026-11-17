<script lang="ts">
  import Alert from '../components/Alert.svelte'
  import Campo from '../components/Campo.svelte'
  import Loading from '../components/Loading.svelte'
  import * as authApi from '../api/auth.api'
  import * as instituicoesApi from '../api/instituicoes.api'
  import { mensagemDeErro } from '../api/http'
  import type { InstituicaoPublica } from '../models/instituicao.model'
  import { auth } from '../state/auth.svelte'
  import { router } from '../state/router.svelte'
  import { numeroOuNull, textoOuNull } from '../utils/formatar'

  type Tipo = 'atleta' | 'treinador' | 'coordenador'

  const opcoes: { tipo: Tipo; rotulo: string; descricao: string }[] = [
    { tipo: 'atleta', rotulo: 'Atleta', descricao: 'Participe de esportes e treinos.' },
    { tipo: 'treinador', rotulo: 'Treinador', descricao: 'Precisa da aprovação do coordenador.' },
    { tipo: 'coordenador', rotulo: 'Coordenador', descricao: 'Precisa da aprovação do administrador.' },
  ]

  let tipo = $state<Tipo>('atleta')

  // Campos comuns
  let nome = $state('')
  let email = $state('')
  let senha = $state('')
  let bio = $state('')
  // Atleta
  let ano = $state('')
  // Treinador
  let instituicaoId = $state('')
  // Coordenador
  let nomeInstituicao = $state('')
  let descricaoInstituicao = $state('')
  let latitude = $state('')
  let longitude = $state('')

  let instituicoes = $state<InstituicaoPublica[]>([])
  let carregandoInstituicoes = $state(false)
  let instituicoesCarregadas = $state(false)
  let erro = $state('')
  let enviando = $state(false)

  async function escolherTipo(novo: Tipo) {
    tipo = novo
    erro = ''
    if (novo === 'treinador' && !instituicoesCarregadas) {
      carregandoInstituicoes = true
      try {
        instituicoes = await instituicoesApi.listarPublicas()
        instituicoesCarregadas = true
      } catch (e) {
        erro = mensagemDeErro(e)
      } finally {
        carregandoInstituicoes = false
      }
    }
  }

  async function enviar(evento: Event) {
    evento.preventDefault()
    erro = ''

    if (senha.length < 8) {
      erro = 'A senha precisa ter pelo menos 8 caracteres.'
      return
    }

    enviando = true
    try {
      const base = {
        email: email.trim(),
        password: senha,
        nome: nome.trim(),
        bio: textoOuNull(bio),
      }

      if (tipo === 'atleta') {
        const anoNumero = numeroOuNull(ano)
        if (anoNumero === null || !Number.isInteger(anoNumero)) {
          erro = 'Informe o ano como um número inteiro.'
          return
        }
        await authApi.cadastrarAtleta({ ...base, ano: anoNumero })
      } else if (tipo === 'treinador') {
        if (instituicaoId === '') {
          erro = 'Escolha a instituição onde você vai treinar.'
          return
        }
        await authApi.cadastrarTreinador({ ...base, institution_id: instituicaoId })
      } else {
        await authApi.cadastrarCoordenador({
          ...base,
          institution_name: nomeInstituicao.trim(),
          institution_description: textoOuNull(descricaoInstituicao),
          institution_latitude: numeroOuNull(latitude),
          institution_longitude: numeroOuNull(longitude),
        })
      }

      auth.aviso =
        tipo === 'atleta'
          ? 'Cadastro realizado! Entre com seu e-mail e senha.'
          : 'Cadastro enviado! Entre para acompanhar a aprovação da sua solicitação.'
      router.navegar('login')
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      enviando = false
    }
  }
</script>

<div class="flex min-h-screen items-start justify-center bg-slate-100 p-4 sm:items-center sm:p-6">
  <div class="w-full max-w-2xl">
    <div class="mb-5 flex items-center gap-2 text-xl font-bold text-slate-900">
      <span class="grid h-9 w-9 place-items-center rounded-full bg-emerald-600 text-white">⚽</span>
      TCA Esportando
    </div>

    <div class="cartao">
      <h1 class="text-2xl font-bold text-slate-900">Criar conta</h1>
      <p class="mb-5 mt-1 text-sm text-slate-500">Escolha como você vai usar o sistema.</p>

      <div class="mb-6 grid gap-3 sm:grid-cols-3">
        {#each opcoes as opcao (opcao.tipo)}
          <button
            type="button"
            class="rounded-xl border-2 p-3 text-left transition {tipo === opcao.tipo
              ? 'border-emerald-600 bg-emerald-50'
              : 'border-slate-200 hover:border-slate-300'}"
            onclick={() => escolherTipo(opcao.tipo)}
          >
            <p class="font-semibold text-slate-900">{opcao.rotulo}</p>
            <p class="mt-0.5 text-xs text-slate-500">{opcao.descricao}</p>
          </button>
        {/each}
      </div>

      <form class="space-y-4" onsubmit={enviar}>
        <Alert tipo="erro" mensagem={erro} />

        <div class="grid gap-4 sm:grid-cols-2">
          <Campo rotulo="Nome completo" bind:valor={nome} obrigatorio maxlength={100} autocomplete="name" />
          <Campo rotulo="E-mail" tipo="email" bind:valor={email} obrigatorio autocomplete="email" />
          <Campo
            rotulo="Senha"
            tipo="password"
            bind:valor={senha}
            obrigatorio
            autocomplete="new-password"
            ajuda="Mínimo de 8 caracteres."
          />

          {#if tipo === 'atleta'}
            <Campo
              rotulo="Ano"
              tipo="number"
              bind:valor={ano}
              obrigatorio
              min={1}
              step={1}
              placeholder="Ex.: 2"
              ajuda="Número inteiro."
            />
          {/if}
        </div>

        {#if tipo === 'treinador'}
          <div>
            <label class="block">
              <span class="rotulo">Instituição <span class="text-red-500">*</span></span>
              {#if carregandoInstituicoes}
                <Loading texto="Carregando instituições..." />
              {:else}
                <select class="campo" bind:value={instituicaoId} required>
                  <option value="" disabled>Selecione a instituição</option>
                  {#each instituicoes as instituicao (instituicao.id)}
                    <option value={instituicao.id}>{instituicao.nome}</option>
                  {/each}
                </select>
              {/if}
            </label>
            {#if instituicoesCarregadas && instituicoes.length === 0}
              <p class="ajuda">
                Nenhuma instituição disponível ainda. Uma instituição só aparece depois que o
                administrador aprova o coordenador dela.
              </p>
            {/if}
          </div>
        {/if}

        {#if tipo === 'coordenador'}
          <fieldset class="space-y-4 rounded-xl border border-slate-200 p-4">
            <legend class="px-2 text-sm font-semibold text-slate-700">
              Instituição que você quer criar
            </legend>
            <Campo
              rotulo="Nome da instituição"
              bind:valor={nomeInstituicao}
              obrigatorio
              maxlength={100}
            />
            <label class="block">
              <span class="rotulo">Descrição</span>
              <textarea
                class="campo"
                rows="2"
                maxlength="1024"
                bind:value={descricaoInstituicao}
              ></textarea>
            </label>
            <div class="grid gap-4 sm:grid-cols-2">
              <Campo rotulo="Latitude (opcional)" bind:valor={latitude} placeholder="-25.5163" />
              <Campo rotulo="Longitude (opcional)" bind:valor={longitude} placeholder="-48.5225" />
            </div>
            <p class="ajuda">A instituição só é criada depois que o administrador aprovar o seu pedido.</p>
          </fieldset>
        {/if}

        <label class="block">
          <span class="rotulo">Sobre você (opcional)</span>
          <textarea class="campo" rows="3" maxlength="1024" bind:value={bio}></textarea>
        </label>

        <div class="flex flex-col-reverse gap-3 sm:flex-row sm:justify-between">
          <button type="button" class="btn-claro" onclick={() => router.navegar('login')}>
            Já tenho conta
          </button>
          <button type="submit" class="btn-primario" disabled={enviando}>
            {enviando ? 'Enviando...' : 'Criar conta'}
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
