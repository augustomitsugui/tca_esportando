<script>
  import Icon from './Icon.svelte';

  export let title;
  export let subtitle = '';
  export let icon = '';
</script>

<header class="mb-6 flex flex-wrap items-center gap-4">
  {#if icon}
    <span class="grid h-14 w-14 place-items-center rounded-2xl bg-accent-600 text-white shadow-soft">
      <Icon name={icon} size={30} />
    </span>
  {/if}
  <div class="min-w-0 flex-1">
    <h1 class="sport-title text-4xl leading-none text-brand-800">{title}</h1>
    {#if subtitle}<p class="mt-1 text-ink-500">{subtitle}</p>{/if}
  </div>
  <div class="flex flex-wrap gap-2"><slot /></div>
</header>
