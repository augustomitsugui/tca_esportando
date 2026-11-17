<script>
  import Icon from './Icon.svelte';

  export let label = '';
  export let name = '';
  export let value = '';
  export let options = []; // [{ value, label }]
  export let placeholder = 'Selecione...';
  export let hint = '';
  export let required = false;
  export let disabled = false;

  const id = `s-${name}-${Math.random().toString(36).slice(2, 7)}`;
</script>

<div>
  <label for={id} class="mb-1.5 block text-sm font-semibold text-ink-700">
    {label}{#if required}<span class="text-accent-600"> *</span>{/if}
  </label>
  <div class="relative">
    <select
      {id}
      {name}
      {required}
      {disabled}
      class="field-input appearance-none pr-11"
      on:change={(e) => (value = e.currentTarget.value)}
    >
      <option value="" selected={!value}>{placeholder}</option>
      {#each options as option}
        <option value={option.value} selected={option.value === value}>
          {option.label}
        </option>
      {/each}
    </select>
    <span class="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-brand-500">
      <Icon name="expand_more" size={22} />
    </span>
  </div>
  {#if hint}<p class="mt-1 text-xs text-ink-500">{hint}</p>{/if}
</div>
