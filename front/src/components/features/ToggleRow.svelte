<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from '../ui/Icon.svelte';

  export let label;
  export let description = '';
  export let linked = false;
  export let busy = false;

  const dispatch = createEventDispatcher();
</script>

<div class="flex items-center gap-3 rounded-2xl border border-brand-100 px-4 py-3 {linked ? 'bg-brand-50' : 'bg-white'}">
  <div class="min-w-0 flex-1">
    <p class="font-bold text-ink-900">{label}</p>
    {#if description}<p class="line-clamp-1 text-sm text-ink-500">{description}</p>{/if}
  </div>
  <button
    type="button"
    disabled={busy}
    aria-pressed={linked}
    class="flex items-center gap-1.5 rounded-full px-4 py-1.5 font-display text-sm font-bold uppercase tracking-wider transition active:scale-95 disabled:opacity-50 {linked
      ? 'bg-accent-50 text-accent-700 hover:bg-accent-100'
      : 'bg-brand-600 text-white hover:bg-brand-700'}"
    on:click={() => dispatch('toggle')}
  >
    <Icon name={linked ? 'link_off' : 'link'} size={18} />
    {linked ? 'Desvincular' : 'Vincular'}
  </button>
</div>
