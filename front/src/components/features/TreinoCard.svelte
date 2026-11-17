<script>
  import Card from '../ui/Card.svelte';
  import Icon from '../ui/Icon.svelte';
  import { dateParts } from '../../lib/format.js';

  export let nome;
  export let dataHora;
  export let esporte = '';
  export let local = '';
  export let treinador = '';
  export let descricao = '';

  $: parts = dateParts(dataHora);
</script>

<Card hover class="flex gap-4">
  <div class="flex h-20 w-20 shrink-0 flex-col items-center justify-center rounded-2xl bg-accent-600 text-white">
    <span class="sport-title text-3xl leading-none">{parts.day}</span>
    <span class="text-xs font-bold uppercase tracking-wider">{parts.month}</span>
  </div>
  <div class="min-w-0 flex-1">
    <h3 class="sport-title truncate text-2xl text-brand-800">{nome}</h3>
    {#if esporte}
      <p class="text-sm font-semibold text-accent-700">{esporte}</p>
    {/if}
    {#if descricao}<p class="mt-1 line-clamp-2 text-sm text-ink-500">{descricao}</p>{/if}
    <ul class="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-ink-600">
      <li class="flex items-center gap-1"><Icon name="schedule" size={18} class="text-brand-500" />{parts.time}</li>
      {#if local}<li class="flex items-center gap-1"><Icon name="location_on" size={18} class="text-brand-500" />{local}</li>{/if}
      {#if treinador}<li class="flex items-center gap-1"><Icon name="sports" size={18} class="text-brand-500" />{treinador}</li>{/if}
    </ul>
  </div>
</Card>
