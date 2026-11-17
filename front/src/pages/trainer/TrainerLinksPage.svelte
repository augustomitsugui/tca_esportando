<script>
  import { onMount } from 'svelte';
  import { vinculoService } from '../../services/vinculoService.js';
  import { errorMessage } from '../../services/api.js';
  import { toast } from '../../stores/toast.js';
  import PageHeader from '../../components/ui/PageHeader.svelte';
  import Button from '../../components/ui/Button.svelte';
  import Spinner from '../../components/ui/Spinner.svelte';
  import Alert from '../../components/ui/Alert.svelte';
  import EmptyState from '../../components/ui/EmptyState.svelte';
  import VinculoCard from '../../components/features/VinculoCard.svelte';

  // mode: 'pending' (pedidos de atletas) | 'approved' (atletas vinculados)
  export let mode;

  let items = [];
  let loading = true;
  let error = '';
  let busyId = null;

  $: pendingMode = mode === 'pending';

  async function load() {
    loading = true;
    error = '';
    try {
      items = pendingMode
        ? await vinculoService.trainerPending()
        : await vinculoService.trainerAthletes();
    } catch (err) {
      error = errorMessage(err);
    } finally {
      loading = false;
    }
  }

  async function decide(vinculo, status) {
    busyId = vinculo.id;
    try {
      await vinculoService.decide(vinculo.id, status);
      toast.success(status === 'aprovado' ? 'Atleta aprovado!' : 'Pedido recusado.');
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      busyId = null;
    }
  }

  onMount(load);
</script>

<PageHeader
  title={pendingMode ? 'Pedidos de atletas' : 'Meus atletas'}
  subtitle={pendingMode ? 'Atletas querendo entrar nos seus esportes.' : 'Atletas vinculados aos seus esportes.'}
  icon={pendingMode ? 'mark_email_unread' : 'groups'}
/>

{#if loading}
  <Spinner />
{:else if error}
  <Alert message={error} />
{:else if items.length === 0}
  <EmptyState
    icon={pendingMode ? 'inbox' : 'groups'}
    title={pendingMode ? 'Nenhum pedido no momento' : 'Nenhum atleta vinculado'}
  />
{:else}
  <div class="grid gap-4 lg:grid-cols-2">
    {#each items as vinculo (vinculo.id)}
      <VinculoCard {vinculo} showAthlete>
        {#if pendingMode}
          <Button variant="danger" size="sm" icon="close" disabled={busyId === vinculo.id} on:click={() => decide(vinculo, 'recusado')}>Recusar</Button>
          <Button size="sm" icon="check" loading={busyId === vinculo.id} on:click={() => decide(vinculo, 'aprovado')}>Aprovar</Button>
        {/if}
      </VinculoCard>
    {/each}
  </div>
{/if}
