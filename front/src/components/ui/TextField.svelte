<script>
  import Icon from './Icon.svelte';

  export let label = '';
  export let name = '';
  export let type = 'text';
  export let value = '';
  export let placeholder = '';
  export let hint = '';
  export let icon = '';
  export let required = false;
  export let disabled = false;
  export let maxlength = undefined;
  export let minlength = undefined;
  export let min = undefined;
  export let step = undefined;
  export let autocomplete = undefined;

  const id = `f-${name}-${Math.random().toString(36).slice(2, 7)}`;
</script>

<div>
  <label for={id} class="mb-1.5 block text-sm font-semibold text-ink-700">
    {label}{#if required}<span class="text-accent-600"> *</span>{/if}
  </label>
  <div class="relative">
    {#if icon}
      <span class="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-brand-500">
        <Icon name={icon} size={20} />
      </span>
    {/if}
    <input
      {id}
      {name}
      {type}
      {value}
      {placeholder}
      {required}
      {disabled}
      {maxlength}
      {minlength}
      {min}
      {step}
      {autocomplete}
      class="field-input {icon ? 'pl-11' : ''}"
      on:input={(e) => (value = e.currentTarget.value)}
    />
  </div>
  {#if hint}<p class="mt-1 text-xs text-ink-500">{hint}</p>{/if}
</div>
