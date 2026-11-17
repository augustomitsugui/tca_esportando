<script>
  import { onMount } from 'svelte';
  import { session } from '../../stores/auth.js';
  import { treinoService } from '../../services/treinoService.js';
  import { errorMessage } from '../../services/api.js';
  import PageHeader from '../../components/ui/PageHeader.svelte';
  import Tabs from '../../components/ui/Tabs.svelte';
  import Spinner from '../../components/ui/Spinner.svelte';
  import Alert from '../../components/ui/Alert.svelte';
  import EmptyState from '../../components/ui/EmptyState.svelte';
  import TreinoCard from '../../components/features/TreinoCard.svelte';

  const atletaId = $session.user.profile_id;

  let tab = 'upcoming';
  let upcoming = [];
  let all = [];
  let loading = true;
  let error = '';

  $: tabs = [
    { id: 'upcoming', label: 'Próximos', count: upcoming.length },
    { id: 'all', label: 'Todos', count: all.length },
  ];

  onMount(async () => {
    try {
      [upcoming, all] = await Promise.all([
        treinoService.upcoming(atletaId),
        treinoService.all(atletaId),
      ]);
    } catch (err) {
      error = errorMessage(err);
    } finally {
      loading = false;
    }
  });
</script>

<PageHeader title="Meus treinos" subtitle="Sua agenda de treinos." icon="event" />

{#if loading}
  <Spinner />
{:else if error}
  <Alert message={error} />
{:else}
  <Tabs {tabs} bind:active={tab} />

  {#if tab === 'upcoming'}
    {#if upcoming.length === 0}
      <EmptyState icon="event_busy" title="Sem treinos marcados" text="Os próximos treinos aparecem aqui." />
    {:else}
      <div class="grid gap-4 lg:grid-cols-2">
        {#each upcoming as t (t.treino_id)}
          <TreinoCard nome={t.treino_nome} dataHora={t.data_hora} esporte={t.esporte_nome} local={t.local_nome} treinador={t.treinador_nome} />
        {/each}
      </div>
    {/if}
  {:else if all.length === 0}
    <EmptyState icon="event_busy" title="Nenhum treino ainda" />
  {:else}
    <div class="grid gap-4 lg:grid-cols-2">
      {#each all as t (t.id)}
        <TreinoCard nome={t.nome} dataHora={t.data_hora} descricao={t.descricao ?? ''} />
      {/each}
    </div>
  {/if}
{/if}
