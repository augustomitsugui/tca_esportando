<script>
  import Icon from './Icon.svelte';

  export let icon = 'sports_score';
  export let title = 'Nada por aqui ainda';
  export let text = '';
</script>

<div class="flex flex-col items-center gap-2 px-6 py-12 text-center">
  <span class="grid h-20 w-20 place-items-center rounded-full bg-brand-50 text-brand-500">
    <Icon name={icon} size={40} />
  </span>
  <h3 class="sport-title text-2xl text-brand-800">{title}</h3>
  {#if text}<p class="max-w-sm text-ink-500">{text}</p>{/if}
  <div class="mt-3"><slot /></div>
</div>
