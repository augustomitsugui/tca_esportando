<script>
  import Card from '../ui/Card.svelte';
  import Icon from '../ui/Icon.svelte';
  import Avatar from '../ui/Avatar.svelte';
  import StatusBadge from '../ui/StatusBadge.svelte';

  // Vínculo atleta <-> esporte
  export let vinculo;
  export let showAthlete = false; // visão do treinador mostra o atleta
</script>

<Card hover class="flex flex-wrap items-center gap-4">
  {#if showAthlete}
    <Avatar name={vinculo.atleta_nome ?? '?'} size={48} />
  {:else}
    <span class="grid h-12 w-12 place-items-center rounded-full bg-brand-100 text-brand-700">
      <Icon name="sports_soccer" size={26} />
    </span>
  {/if}

  <div class="min-w-0 flex-1">
    <h3 class="sport-title truncate text-2xl text-brand-800">
      {showAthlete ? (vinculo.atleta_nome ?? 'Atleta') : (vinculo.esporte_nome ?? 'Esporte')}
    </h3>
    {#if showAthlete}
      <p class="text-sm text-ink-500">quer participar de <strong class="text-accent-700">{vinculo.esporte_nome}</strong></p>
    {/if}
  </div>

  <StatusBadge status={vinculo.status} />
  <div class="flex gap-2"><slot /></div>
</Card>
