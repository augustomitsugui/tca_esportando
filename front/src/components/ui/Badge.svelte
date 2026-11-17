<script>
  import Icon from './Icon.svelte';

  export let tone = 'gray'; // green | red | amber | gray
  export let icon = '';

  const tones = {
    green: 'bg-brand-100 text-brand-800',
    red: 'bg-accent-100 text-accent-700',
    amber: 'bg-amber-100 text-amber-800',
    gray: 'bg-gray-100 text-ink-600',
  };
</script>

<span
  class="inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wide {tones[tone]}"
>
  {#if icon}<Icon name={icon} size={14} />{/if}
  <slot />
</span>
