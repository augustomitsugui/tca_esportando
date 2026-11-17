<script>
  import Card from './Card.svelte';
  import Icon from './Icon.svelte';

  export let label;
  export let value = null; // null = carregando / indisponível
  export let icon = 'sports_score';
  export let tone = 'green'; // green | red

  const tones = {
    green: 'bg-brand-100 text-brand-700',
    red: 'bg-accent-100 text-accent-600',
  };
</script>

<Card hover>
  <div class="flex items-center gap-4">
    <span class="grid h-14 w-14 shrink-0 place-items-center rounded-2xl {tones[tone]}">
      <Icon name={icon} size={30} />
    </span>
    <div>
      <p class="sport-title text-4xl leading-none text-ink-900">{value ?? '—'}</p>
      <p class="mt-1 text-sm font-semibold text-ink-500">{label}</p>
    </div>
  </div>
</Card>
