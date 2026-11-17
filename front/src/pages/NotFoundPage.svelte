<script>
  import Link from '../router/Link.svelte';
  import Card from '../components/ui/Card.svelte';
  import Icon from '../components/ui/Icon.svelte';
</script>

<Card class="space-y-4 p-10 text-center">
  <Icon name="sports_score" size={64} class="mx-auto text-accent-600" />
  <h1 class="sport-title text-7xl text-brand-800">404</h1>
  <p class="text-ink-500">Essa jogada saiu pela linha de fundo. A página não foi encontrada.</p>
  <Link
    to="/"
    class="inline-flex items-center gap-2 rounded-full bg-brand-600 px-6 py-2.5 font-display font-bold uppercase tracking-wider text-white shadow-soft transition hover:bg-brand-700"
  >
    <Icon name="home" size={22} />Voltar ao início
  </Link>
</Card>
