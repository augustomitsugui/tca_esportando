<script>
  import Icon from './Icon.svelte';

  export let tone = 'error'; // error | success | info
  export let message = '';

  const tones = {
    error: { box: 'bg-accent-50 text-accent-800 border-accent-200', icon: 'error' },
    success: { box: 'bg-brand-50 text-brand-800 border-brand-200', icon: 'check_circle' },
    info: { box: 'bg-amber-50 text-amber-800 border-amber-200', icon: 'info' },
  };
</script>

{#if message}
  <div class="flex items-start gap-2 rounded-2xl border px-4 py-3 text-sm font-medium {tones[tone].box}" role="alert">
    <Icon name={tones[tone].icon} size={20} class="mt-px shrink-0" />
    <span>{message}</span>
  </div>
{/if}
