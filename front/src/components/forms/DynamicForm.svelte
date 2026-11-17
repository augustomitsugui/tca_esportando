<script>
  import TextField from '../ui/TextField.svelte';
  import TextArea from '../ui/TextArea.svelte';
  import SelectField from '../ui/SelectField.svelte';

  // Renderiza os campos declarados em config/resources.js
  export let fields = [];
  export let values = {};
  export let options = {}; // { [campo]: [{ value, label }] }
</script>

<div class="space-y-4">
  {#each fields as f (f.key)}
    {#if f.type === 'textarea'}
      <TextArea label={f.label} name={f.key} bind:value={values[f.key]} maxlength={f.maxlength} required={f.required} />
    {:else if f.type === 'select'}
      <SelectField label={f.label} name={f.key} bind:value={values[f.key]} options={options[f.key] ?? []} required={f.required} />
    {:else}
      <TextField
        label={f.label}
        name={f.key}
        type={f.type === 'datetime' ? 'datetime-local' : (f.type ?? 'text')}
        icon={f.icon ?? ''}
        step={f.step}
        maxlength={f.maxlength}
        required={f.required}
        bind:value={values[f.key]}
      />
    {/if}
  {/each}
</div>
