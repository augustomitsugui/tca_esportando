<script>
  import { onMount } from 'svelte';
  import { roleRequestService } from '../../services/roleRequestService.js';
  import { errorMessage } from '../../services/api.js';
  import { toast } from '../../stores/toast.js';
  import PageHeader from '../../components/ui/PageHeader.svelte';
  import Tabs from '../../components/ui/Tabs.svelte';
  import Spinner from '../../components/ui/Spinner.svelte';
  import Alert from '../../components/ui/Alert.svelte';
  import EmptyState from '../../components/ui/EmptyState.svelte';
  import ConfirmDialog from '../../components/ui/ConfirmDialog.svelte';
  import RequestCard from '../../components/features/RequestCard.svelte';

  // mode: 'coordenador' (pendentes + histórico) | 'admin' (pendentes)
  export let mode;

  let tab = 'pending';
  let pending = [];
  let history = [];
  let loading = true;
  let error = '';
  let busyId = null;

  let rejecting = null;
  let reason = '';

  $: tabs = [
    { id: 'pending', label: 'Pendentes', count: pending.length },
    ...(mode === 'coordenador' ? [{ id: 'history', label: 'Histórico' }] : []),
  ];
  $: list = tab === 'pending' ? pending : history;

  async function load() {
    loading = true;
    error = '';
    try {
      if (mode === 'admin') {
        pending = await roleRequestService.pendingForAdmin();
      } else {
        [pending, history] = await Promise.all([
          roleRequestService.pendingForCoordinator(),
          roleRequestService.coordinatorHistory(),
        ]);
      }
    } catch (err) {
      error = errorMessage(err);
    } finally {
      loading = false;
    }
  }

  async function approve(event) {
    busyId = event.detail.id;
    try {
      await roleRequestService.approve(event.detail.id);
      toast.success('Solicitação aprovada!');
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      busyId = null;
    }
  }

  async function confirmReject() {
    busyId = rejecting.id;
    try {
      await roleRequestService.reject(rejecting.id, reason);
      toast.success('Solicitação recusada.');
      rejecting = null;
      reason = '';
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
  title={mode === 'admin' ? 'Solicitações' : 'Pedidos de treinadores'}
  subtitle={mode === 'admin' ? 'Aprove ou recuse quem quer entrar no sistema.' : 'Aprove ou recuse treinadores da sua instituição.'}
  icon="how_to_reg"
/>

{#if loading}
  <Spinner />
{:else if error}
  <Alert message={error} />
{:else}
  {#if tabs.length > 1}<Tabs {tabs} bind:active={tab} />{/if}

  {#if list.length === 0}
    <EmptyState icon="inbox" title="Nada por aqui" text="Nenhuma solicitação nesta lista." />
  {:else}
    <div class="grid gap-4 lg:grid-cols-2">
      {#each list as request (request.id)}
        <RequestCard
          {request}
          actionable={tab === 'pending'}
          busy={busyId === request.id}
          on:approve={approve}
          on:reject={(e) => (rejecting = e.detail)}
        />
      {/each}
    </div>
  {/if}
{/if}

<ConfirmDialog
  open={rejecting !== null}
  title="Recusar solicitação"
  message="Explique o motivo da recusa."
  confirmLabel="Recusar"
  askReason
  loading={busyId !== null && rejecting !== null}
  bind:reason
  on:cancel={() => {
    rejecting = null;
    reason = '';
  }}
  on:confirm={confirmReject}
/>
