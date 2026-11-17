<script>
  import { onMount } from 'svelte';
  import { vinculoService } from '../../services/vinculoService.js';
  import { errorMessage } from '../../services/api.js';
  import { toast } from '../../stores/toast.js';
  import PageHeader from '../../components/ui/PageHeader.svelte';
  import Tabs from '../../components/ui/Tabs.svelte';
  import Button from '../../components/ui/Button.svelte';
  import Badge from '../../components/ui/Badge.svelte';
  import Spinner from '../../components/ui/Spinner.svelte';
  import Alert from '../../components/ui/Alert.svelte';
  import EmptyState from '../../components/ui/EmptyState.svelte';
  import SportCard from '../../components/features/SportCard.svelte';
  import VinculoCard from '../../components/features/VinculoCard.svelte';

  let tab = 'available';
  let available = [];
  let pending = [];
  let approved = [];
  let loading = true;
  let error = '';
  let busyId = null;

  $: tabs = [
    { id: 'available', label: 'Disponíveis', count: available.length },
    { id: 'pending', label: 'Pedidos', count: pending.length },
    { id: 'approved', label: 'Meus esportes', count: approved.length },
  ];
  $: requestedIds = new Set([...pending, ...approved].map((v) => v.esporte_id));

  async function load() {
    loading = true;
    error = '';
    try {
      [available, pending, approved] = await Promise.all([
        vinculoService.available(),
        vinculoService.pending(),
        vinculoService.approved(),
      ]);
    } catch (err) {
      error = errorMessage(err);
    } finally {
      loading = false;
    }
  }

  async function run(id, action, message) {
    busyId = id;
    try {
      await action();
      toast.success(message);
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      busyId = null;
    }
  }

  const request = (sport) =>
    run(sport.id, () => vinculoService.request(sport.id), 'Pedido enviado ao treinador!');
  const cancel = (vinculo) =>
    run(vinculo.id, () => vinculoService.cancel(vinculo.id), 'Pedido cancelado.');

  onMount(load);
</script>

<PageHeader title="Esportes" subtitle="Escolha um esporte e peça para participar." icon="sports_soccer" />

{#if loading}
  <Spinner />
{:else if error}
  <Alert message={error} />
{:else}
  <Tabs {tabs} bind:active={tab} />

  {#if tab === 'available'}
    {#if available.length === 0}
      <EmptyState title="Sem esportes disponíveis" text="Quando houver novos esportes, eles aparecem aqui." />
    {:else}
      <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {#each available as sport (sport.id)}
          <SportCard nome={sport.nome} descricao={sport.descricao ?? ''}>
            {#if requestedIds.has(sport.id)}
              <Badge tone="amber" icon="hourglass_top">Já solicitado</Badge>
            {:else}
              <Button size="sm" icon="add" loading={busyId === sport.id} on:click={() => request(sport)}>Quero participar</Button>
            {/if}
          </SportCard>
        {/each}
      </div>
    {/if}
  {:else if tab === 'pending'}
    {#if pending.length === 0}
      <EmptyState icon="inbox" title="Nenhum pedido pendente" />
    {:else}
      <div class="grid gap-4 lg:grid-cols-2">
        {#each pending as vinculo (vinculo.id)}
          <VinculoCard {vinculo}>
            <Button variant="danger" size="sm" icon="close" loading={busyId === vinculo.id} on:click={() => cancel(vinculo)}>Cancelar</Button>
          </VinculoCard>
        {/each}
      </div>
    {/if}
  {:else if approved.length === 0}
    <EmptyState icon="emoji_events" title="Você ainda não está em nenhum esporte" text="Peça para participar na aba Disponíveis." />
  {:else}
    <div class="grid gap-4 lg:grid-cols-2">
      {#each approved as vinculo (vinculo.id)}
        <VinculoCard {vinculo} />
      {/each}
    </div>
  {/if}
{/if}
