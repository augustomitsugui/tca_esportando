<script>
  import { toasts, dismiss } from '../../stores/toast.js';
  import Icon from './Icon.svelte';

  const tones = {
    success: 'bg-brand-700 text-white',
    error: 'bg-accent-700 text-white',
  };
  const icons = { success: 'check_circle', error: 'error' };
</script>

<div class="pointer-events-none fixed bottom-4 right-4 z-[60] flex w-[min(92vw,22rem)] flex-col gap-2">
  {#each $toasts as t (t.id)}
    <div
      class="pointer-events-auto flex animate-slide-in items-center gap-3 rounded-2xl px-4 py-3 shadow-lift {tones[t.tone]}"
      role="status"
    >
      <Icon name={icons[t.tone]} size={22} filled />
      <p class="flex-1 text-sm font-semibold">{t.message}</p>
      <button type="button" aria-label="Fechar aviso" class="opacity-80 hover:opacity-100" on:click={() => dismiss(t.id)}>
        <Icon name="close" size={18} />
      </button>
    </div>
  {/each}
</div>
