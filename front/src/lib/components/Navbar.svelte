<script lang="ts">
  import { auth } from '../state/auth.svelte'
  import type { Perfil } from '../state/auth.svelte'
  import { router } from '../state/router.svelte'

  let { paginaAtual }: { paginaAtual: string } = $props()

  const menus: Record<Perfil, { pagina: string; rotulo: string }[]> = {
    atleta: [
      { pagina: 'inicio', rotulo: 'Início' },
      { pagina: 'esportes', rotulo: 'Meus esportes' },
      { pagina: 'treinos', rotulo: 'Meus treinos' },
    ],
    treinador: [
      { pagina: 'inicio', rotulo: 'Início' },
      { pagina: 'esportes', rotulo: 'Esportes' },
      { pagina: 'treinos', rotulo: 'Treinos' },
      { pagina: 'atletas', rotulo: 'Atletas' },
    ],
    coordenador: [
      { pagina: 'inicio', rotulo: 'Início' },
      { pagina: 'solicitacoes', rotulo: 'Solicitações' },
      { pagina: 'instituicao', rotulo: 'Instituição' },
      { pagina: 'locais', rotulo: 'Locais' },
    ],
    admin: [
      { pagina: 'inicio', rotulo: 'Início' },
      { pagina: 'solicitacoes', rotulo: 'Solicitações' },
      { pagina: 'instituicoes', rotulo: 'Instituições' },
    ],
    pendente: [{ pagina: 'inicio', rotulo: 'Minha solicitação' }],
  }

  const nomesPerfil: Record<Perfil, string> = {
    atleta: 'Atleta',
    treinador: 'Treinador',
    coordenador: 'Coordenador',
    admin: 'Administrador',
    pendente: 'Aguardando aprovação',
  }

  let aberto = $state(false)
  const itens = $derived(auth.perfil ? menus[auth.perfil] : [])

  function ir(pagina: string) {
    router.navegar(pagina)
    aberto = false
  }
</script>

<header class="sticky top-0 z-20 bg-slate-900 text-white shadow">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
    <button
      class="flex items-center gap-2 text-lg font-bold tracking-tight"
      onclick={() => ir('inicio')}
    >
      <span class="grid h-8 w-8 place-items-center rounded-full bg-emerald-500 text-sm">⚽</span>
      TCA Esportando
    </button>

    <button
      class="rounded-lg p-2 hover:bg-slate-800 md:hidden"
      aria-label="Abrir menu"
      aria-expanded={aberto}
      onclick={() => (aberto = !aberto)}
    >
      <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <nav class="hidden items-center gap-1 md:flex">
      {#each itens as item (item.pagina)}
        <button
          class="rounded-lg px-3 py-2 text-sm font-medium transition hover:bg-slate-800 {paginaAtual ===
          item.pagina
            ? 'bg-slate-800 text-emerald-400'
            : 'text-slate-200'}"
          onclick={() => ir(item.pagina)}
        >
          {item.rotulo}
        </button>
      {/each}
    </nav>

    <div class="hidden items-center gap-3 md:flex">
      <div class="text-right leading-tight">
        <p class="max-w-48 truncate text-xs text-slate-300">{auth.usuario?.email}</p>
        <p class="text-xs font-semibold text-emerald-400">
          {auth.perfil ? nomesPerfil[auth.perfil] : ''}
        </p>
      </div>
      <button class="btn-claro btn-pequeno" onclick={() => auth.sair()}>Sair</button>
    </div>
  </div>

  {#if aberto}
    <div class="border-t border-slate-800 px-4 pb-4 md:hidden">
      <nav class="flex flex-col gap-1 py-3">
        {#each itens as item (item.pagina)}
          <button
            class="rounded-lg px-3 py-2 text-left text-sm font-medium hover:bg-slate-800 {paginaAtual ===
            item.pagina
              ? 'bg-slate-800 text-emerald-400'
              : 'text-slate-200'}"
            onclick={() => ir(item.pagina)}
          >
            {item.rotulo}
          </button>
        {/each}
      </nav>
      <p class="truncate text-xs text-slate-300">{auth.usuario?.email}</p>
      <p class="mb-3 text-xs font-semibold text-emerald-400">
        {auth.perfil ? nomesPerfil[auth.perfil] : ''}
      </p>
      <button class="btn-claro w-full" onclick={() => auth.sair()}>Sair</button>
    </div>
  {/if}
</header>
