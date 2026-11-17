<script>
  import Icon from './Icon.svelte';

  export let light = false;
  export let compact = false;
</script>

<div class="flex select-none items-center gap-2.5">
  <span
    class="grid h-10 w-10 place-items-center rounded-2xl shadow-soft {light
      ? 'bg-white text-brand-700'
      : 'bg-brand-600 text-white'}"
  >
    <Icon name="sports_soccer" size={26} filled />
  </span>
  {#if !compact}
    <span
      class="sport-title text-3xl leading-none {light ? 'text-white' : 'text-brand-800'}"
    >
      Espor<span class={light ? 'text-accent-200' : 'text-accent-600'}>tando</span>
    </span>
  {/if}
</div>
