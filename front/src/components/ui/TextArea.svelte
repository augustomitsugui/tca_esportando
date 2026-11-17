<script>
  export let label = '';
  export let name = '';
  export let value = '';
  export let placeholder = '';
  export let hint = '';
  export let required = false;
  export let disabled = false;
  export let maxlength = undefined;
  export let rows = 3;

  const id = `t-${name}-${Math.random().toString(36).slice(2, 7)}`;
</script>

<div>
  <label for={id} class="mb-1.5 block text-sm font-semibold text-ink-700">
    {label}{#if required}<span class="text-accent-600"> *</span>{/if}
  </label>
  <textarea
    {id}
    {name}
    {rows}
    {placeholder}
    {required}
    {disabled}
    {maxlength}
    class="field-input resize-y"
    {value}
    on:input={(e) => (value = e.currentTarget.value)}
  ></textarea>
  {#if hint}<p class="mt-1 text-xs text-ink-500">{hint}</p>{/if}
</div>
