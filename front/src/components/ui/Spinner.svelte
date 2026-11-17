<script>
  import Icon from './Icon.svelte';

  export let label = 'Carregando...';
</script>

<div class="flex flex-col items-center gap-3 py-12 text-brand-600" role="status">
  <Icon name="sports_soccer" size={48} filled class="animate-spin" />
  <p class="font-display text-lg font-bold uppercase tracking-wider">{label}</p>
</div>
