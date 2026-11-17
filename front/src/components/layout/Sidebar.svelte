<script>
  import { createEventDispatcher } from 'svelte';
  import Link from '../../router/Link.svelte';
  import { location } from '../../router/router.js';
  import Logo from '../ui/Logo.svelte';
  import Icon from '../ui/Icon.svelte';

  export let items = [];
  export let open = false; // gaveta no mobile

  const dispatch = createEventDispatcher();

  const isActive = (item, path) =>
    item.exact ? path === item.to : path === item.to || path.startsWith(`${item.to}/`);
</script>

{#if open}
  <button
    type="button"
    tabindex="-1"
    aria-label="Fechar menu"
    class="fixed inset-0 z-30 bg-ink-900/50 backdrop-blur-sm lg:hidden"
    on:click={() => dispatch('close')}
  ></button>
{/if}

<aside
  class="stripes fixed inset-y-0 left-0 z-40 flex w-72 flex-col bg-gradient-to-b from-brand-700 to-brand-900 p-5 text-white transition-transform duration-200 lg:translate-x-0 {open
    ? 'translate-x-0'
    : '-translate-x-full'}"
>
  <div class="mb-8 flex items-center justify-between">
    <Logo light />
    <button type="button" aria-label="Fechar menu" class="rounded-full p-1 hover:bg-white/10 lg:hidden" on:click={() => dispatch('close')}>
      <Icon name="close" />
    </button>
  </div>

  <nav class="flex flex-1 flex-col gap-1.5 overflow-y-auto">
    {#each items as item}
      {@const active = isActive(item, $location.path)}
      <Link
        to={item.to}
        on:navigate={() => dispatch('close')}
        class="group flex items-center gap-3 rounded-2xl px-4 py-2.5 font-display text-lg font-bold uppercase tracking-wider transition {active
          ? 'bg-white text-brand-800 shadow-soft'
          : 'text-brand-100 hover:bg-white/10'}"
      >
        <Icon name={item.icon} size={24} filled={active} class={active ? 'text-accent-600' : ''} />
        {item.label}
      </Link>
    {/each}
  </nav>

  <div class="mt-4 h-1.5 overflow-hidden rounded-full bg-white/20">
    <div class="h-full w-1/3 rounded-full bg-accent-600"></div>
  </div>
</aside>
