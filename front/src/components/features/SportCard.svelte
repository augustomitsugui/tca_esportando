<script>
  import Card from '../ui/Card.svelte';
  import Icon from '../ui/Icon.svelte';

  export let nome;
  export let descricao = '';
</script>

<Card hover class="flex flex-col gap-3">
  <div class="flex items-start gap-3">
    <span class="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-brand-100 text-brand-700">
      <Icon name="sports_soccer" size={28} />
    </span>
    <div class="min-w-0">
      <h3 class="sport-title text-2xl text-brand-800">{nome}</h3>
      <p class="mt-0.5 line-clamp-3 text-sm text-ink-500">{descricao || 'Sem descrição.'}</p>
    </div>
  </div>
  <div class="mt-auto flex flex-wrap items-center justify-end gap-2"><slot /></div>
</Card>
