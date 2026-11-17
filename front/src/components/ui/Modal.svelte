<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from './Icon.svelte';

  export let open = false;
  export let title = '';
  export let icon = '';
  export let size = 'md'; // sm | md | lg

  const dispatch = createEventDispatcher();
  const widths = { sm: 'max-w-md', md: 'max-w-xl', lg: 'max-w-3xl' };

  const close = () => dispatch('close');
  const onKey = (e) => {
    if (open && e.key === 'Escape') close();
  };
</script>

<svelte:window on:keydown={onKey} />

{#if open}
  <div class="fixed inset-0 z-50 grid place-items-center p-4">
    <button
      type="button"
      tabindex="-1"
      aria-label="Fechar"
      class="absolute inset-0 cursor-default bg-ink-900/50 backdrop-blur-sm"
      on:click={close}
    ></button>

    <div
      role="dialog"
      aria-modal="true"
      aria-label={title}
      class="relative max-h-[90vh] w-full animate-pop overflow-y-auto rounded-3xl bg-white shadow-lift {widths[size]}"
    >
      <header class="stripes flex items-center gap-3 rounded-t-3xl bg-brand-600 px-6 py-4 text-white">
        {#if icon}
          <span class="grid h-10 w-10 place-items-center rounded-2xl bg-white/20">
            <Icon name={icon} size={24} />
          </span>
        {/if}
        <h2 class="sport-title flex-1 text-2xl text-white">{title}</h2>
        <button
          type="button"
          aria-label="Fechar"
          class="grid h-9 w-9 place-items-center rounded-full transition hover:bg-white/20"
          on:click={close}
        >
          <Icon name="close" size={22} />
        </button>
      </header>

      <div class="p-6"><slot /></div>

      {#if $$slots.footer}
        <footer class="flex flex-wrap justify-end gap-3 border-t border-brand-100 px-6 py-4">
          <slot name="footer" />
        </footer>
      {/if}
    </div>
  </div>
{/if}
