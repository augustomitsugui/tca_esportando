<script>
  import Icon from '../ui/Icon.svelte';

  export let value = 'atleta';

  const roles = [
    { id: 'atleta', label: 'Sou atleta', icon: 'directions_run', text: 'Quero treinar' },
    { id: 'treinador', label: 'Sou treinador', icon: 'sports', text: 'Quero orientar' },
    { id: 'coordenador', label: 'Sou coordenador', icon: 'badge', text: 'Quero coordenar' },
  ];
</script>

<div class="grid gap-3 sm:grid-cols-3" role="radiogroup" aria-label="Tipo de conta">
  {#each roles as role}
    {@const selected = value === role.id}
    <button
      type="button"
      role="radio"
      aria-checked={selected}
      class="flex flex-col items-center gap-1 rounded-3xl border-2 px-3 py-4 text-center transition active:scale-95 {selected
        ? 'border-brand-600 bg-brand-600 text-white shadow-lift'
        : 'border-brand-100 bg-white text-ink-700 hover:border-brand-300 hover:bg-brand-50'}"
      on:click={() => (value = role.id)}
    >
      <Icon name={role.icon} size={34} filled={selected} />
      <span class="sport-title text-xl leading-tight">{role.label}</span>
      <span class="text-xs {selected ? 'text-brand-100' : 'text-ink-500'}">{role.text}</span>
    </button>
  {/each}
</div>
