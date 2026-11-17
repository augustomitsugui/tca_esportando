<script>
  import { onMount } from 'svelte';
  import { treinoService } from '../../services/treinoService.js';
  import { errorMessage } from '../../services/api.js';
  import Spinner from '../../components/ui/Spinner.svelte';
  import Alert from '../../components/ui/Alert.svelte';
  import EmptyState from '../../components/ui/EmptyState.svelte';
  import TreinoCard from '../../components/features/TreinoCard.svelte';

  export let atletaId;

  let treinos = [];
  let loading = true;
  let error = '';

  onMount(async () => {
    try {
      treinos = (await treinoService.upcoming(atletaId)).slice(0, 3);
    } catch (err) {
      error = errorMessage(err);
    } finally {
      loading = false;
    }
  });
</script>

<section>
  <h2 class="sport-title mb-3 text-3xl text-brand-800">Próximos treinos</h2>
  {#if loading}
    <Spinner />
  {:else if error}
    <Alert message={error} />
  {:else if treinos.length === 0}
    <EmptyState icon="event_busy" title="Sem treinos por enquanto" text="Quando houver treinos marcados, eles aparecem aqui." />
  {:else}
    <div class="grid gap-4 md:grid-cols-2">
      {#each treinos as t (t.treino_id)}
        <TreinoCard nome={t.treino_nome} dataHora={t.data_hora} esporte={t.esporte_nome} local={t.local_nome} treinador={t.treinador_nome} />
      {/each}
    </div>
  {/if}
</section>
