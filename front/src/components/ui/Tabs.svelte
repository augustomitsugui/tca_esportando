<script>
  export let tabs = []; // [{ id, label, count? }]
  export let active;
</script>

<div class="mb-6 inline-flex max-w-full flex-wrap gap-1 rounded-full border border-brand-100 bg-white p-1 shadow-soft">
  {#each tabs as tab}
    <button
      type="button"
      class="flex items-center gap-2 rounded-full px-5 py-2 font-display text-base font-bold uppercase tracking-wider transition {active === tab.id
        ? 'bg-brand-600 text-white shadow-soft'
        : 'text-ink-600 hover:bg-brand-50'}"
      on:click={() => (active = tab.id)}
    >
      {tab.label}
      {#if tab.count !== undefined}
        <span class="rounded-full px-2 text-sm {active === tab.id ? 'bg-white/25' : 'bg-accent-100 text-accent-700'}">
          {tab.count}
        </span>
      {/if}
    </button>
  {/each}
</div>
