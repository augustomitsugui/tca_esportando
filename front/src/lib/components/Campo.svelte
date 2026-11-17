<script lang="ts">
  import type { HTMLInputAttributes } from 'svelte/elements'

  // Campo de texto reutilizável (rótulo + input).
  // O valor é sempre texto; quem usa converte para número quando precisar.
  let {
    rotulo,
    valor = $bindable(''),
    tipo = 'text',
    placeholder = '',
    obrigatorio = false,
    maxlength,
    min,
    max,
    step,
    ajuda = '',
    autocomplete,
  }: {
    rotulo: string
    valor?: string
    tipo?: string
    placeholder?: string
    obrigatorio?: boolean
    maxlength?: number
    min?: number | string
    max?: number | string
    step?: number | string
    ajuda?: string
    autocomplete?: HTMLInputAttributes['autocomplete']
  } = $props()
</script>

<label class="block">
  <span class="rotulo">{rotulo}{#if obrigatorio}<span class="text-red-500"> *</span>{/if}</span>
  <input
    class="campo"
    type={tipo}
    {placeholder}
    required={obrigatorio}
    {maxlength}
    {min}
    {max}
    {step}
    {autocomplete}
    value={valor}
    oninput={(e) => (valor = e.currentTarget.value)}
  />
  {#if ajuda}<span class="ajuda">{ajuda}</span>{/if}
</label>
