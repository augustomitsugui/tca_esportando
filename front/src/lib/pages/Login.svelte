<script lang="ts">
  import Alert from '../components/Alert.svelte'
  import Campo from '../components/Campo.svelte'
  import { mensagemDeErro } from '../api/http'
  import { auth } from '../state/auth.svelte'
  import { router } from '../state/router.svelte'

  let email = $state('')
  let senha = $state('')
  let erro = $state('')
  let enviando = $state(false)

  async function entrar(evento: Event) {
    evento.preventDefault()
    erro = ''
    enviando = true
    try {
      await auth.entrar(email.trim(), senha)
      auth.aviso = ''
      router.navegar('inicio')
    } catch (e) {
      erro = mensagemDeErro(e)
    } finally {
      enviando = false
    }
  }
</script>

<div class="grid min-h-screen lg:grid-cols-2">
  <!-- Lado esquerdo: apresentação (só aparece em telas grandes) -->
  <div
    class="hidden flex-col justify-between bg-gradient-to-br from-emerald-600 via-emerald-700 to-slate-900 p-12 text-white lg:flex"
  >
    <div class="flex items-center gap-3 text-xl font-bold">
      <span class="grid h-10 w-10 place-items-center rounded-full bg-white/20">⚽</span>
      TCA Esportando
    </div>
    <div>
      <h2 class="text-4xl font-extrabold leading-tight">
        Organize treinos,<br />esportes e atletas<br />em um só lugar.
      </h2>
      <p class="mt-4 max-w-md text-emerald-100">
        Sistema esportivo escolar: atletas se inscrevem, treinadores montam os treinos e
        coordenadores cuidam da instituição.
      </p>
    </div>
    <p class="text-sm text-emerald-200">Projeto TCA · Informática</p>
  </div>

  <!-- Lado direito: formulário -->
  <div class="flex items-center justify-center bg-slate-100 p-6">
    <div class="w-full max-w-md">
      <div class="mb-6 flex items-center gap-2 text-xl font-bold text-slate-900 lg:hidden">
        <span class="grid h-9 w-9 place-items-center rounded-full bg-emerald-600 text-white">⚽</span>
        TCA Esportando
      </div>

      <div class="cartao">
        <h1 class="text-2xl font-bold text-slate-900">Entrar</h1>
        <p class="mb-5 mt-1 text-sm text-slate-500">Use o e-mail e a senha do seu cadastro.</p>

        <form class="space-y-4" onsubmit={entrar}>
          <Alert tipo="info" mensagem={auth.aviso} />
          <Alert tipo="erro" mensagem={erro} />

          <Campo
            rotulo="E-mail"
            tipo="email"
            bind:valor={email}
            obrigatorio
            autocomplete="email"
            placeholder="voce@exemplo.com"
          />
          <Campo
            rotulo="Senha"
            tipo="password"
            bind:valor={senha}
            obrigatorio
            autocomplete="current-password"
          />

          <button type="submit" class="btn-primario w-full" disabled={enviando}>
            {enviando ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <p class="mt-5 text-center text-sm text-slate-600">
          Ainda não tem conta?
          <button
            class="font-semibold text-emerald-700 hover:underline"
            onclick={() => router.navegar('cadastro')}
          >
            Cadastre-se
          </button>
        </p>
      </div>
    </div>
  </div>
</div>
