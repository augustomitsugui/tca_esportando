// src/lib/state/router.svelte.ts
// Navegação simples: a "página atual" fica no endereço (#/nome) e num $state.
// Assim o botão "voltar" e o F5 do navegador continuam funcionando.

function lerPagina(): string {
  const hash = window.location.hash.replace(/^#\/?/, '')
  return hash === '' ? 'inicio' : hash
}

class RouterState {
  pagina = $state(lerPagina())

  constructor() {
    window.addEventListener('hashchange', () => {
      this.pagina = lerPagina()
    })
  }

  navegar(pagina: string) {
    window.location.hash = `#/${pagina}`
  }
}

// Instância única (Singleton), como no exemplo da aula
export const router = new RouterState()
