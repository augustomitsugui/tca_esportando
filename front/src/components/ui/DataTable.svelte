<script>
  import StatusBadge from './StatusBadge.svelte';

  // columns: [{ key, label, render?(row), badge? }]
  export let columns = [];
  export let rows = [];
  export let rowKey = 'id';

  const cell = (col, row) => {
    const value = col.render ? col.render(row) : row[col.key];
    return value === null || value === undefined || value === '' ? '—' : value;
  };
</script>

<div class="overflow-x-auto">
  <table class="w-full text-left">
    <thead>
      <tr class="bg-brand-50">
        {#each columns as col}
          <th class="whitespace-nowrap px-5 py-3 font-display text-sm font-bold uppercase tracking-wider text-brand-700">
            {col.label}
          </th>
        {/each}
        {#if $$slots.actions}<th class="w-px px-5"></th>{/if}
      </tr>
    </thead>
    <tbody>
      {#each rows as row (row[rowKey])}
        <tr class="border-t border-brand-100 transition hover:bg-brand-50/60">
          {#each columns as col}
            <td class="max-w-xs px-5 py-3.5 align-middle text-ink-700">
              {#if col.badge}
                <StatusBadge status={cell(col, row)} />
              {:else}
                <span class="line-clamp-2">{cell(col, row)}</span>
              {/if}
            </td>
          {/each}
          {#if $$slots.actions}
            <td class="whitespace-nowrap px-5 py-2 text-right">
              <slot name="actions" {row} />
            </td>
          {/if}
        </tr>
      {/each}
    </tbody>
  </table>
</div>
