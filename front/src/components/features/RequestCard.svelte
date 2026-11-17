<script>
  import { createEventDispatcher } from 'svelte';
  import Card from '../ui/Card.svelte';
  import Icon from '../ui/Icon.svelte';
  import Button from '../ui/Button.svelte';
  import StatusBadge from '../ui/StatusBadge.svelte';
  import { formatDateTime, shortId } from '../../lib/format.js';

  // Solicitação de cargo (treinador ou coordenador)
  export let request;
  export let actionable = false;
  export let busy = false;

  const dispatch = createEventDispatcher();
  const roles = { treinador: 'Treinador', coordenador: 'Coordenador' };
</script>

<Card hover class="space-y-3">
  <div class="flex flex-wrap items-center gap-3">
    <span class="grid h-12 w-12 place-items-center rounded-2xl bg-brand-100 text-brand-700">
      <Icon name={request.requested_role === 'coordenador' ? 'badge' : 'sports'} size={28} />
    </span>
    <div class="min-w-0 flex-1">
      <h3 class="sport-title text-2xl text-brand-800">
        {roles[request.requested_role] ?? request.requested_role}
      </h3>
      <p class="text-sm text-ink-500">
        Usuário {shortId(request.user_id)} · pedido em {formatDateTime(request.created_at)}
      </p>
    </div>
    <StatusBadge status={request.status} />
  </div>

  {#if request.institution_name}
    <div class="rounded-2xl bg-brand-50 p-3 text-sm">
      <p class="flex items-center gap-1.5 font-bold text-brand-800">
        <Icon name="account_balance" size={18} />{request.institution_name}
      </p>
      {#if request.institution_description}
        <p class="mt-1 text-ink-600">{request.institution_description}</p>
      {/if}
      {#if request.institution_latitude !== null && request.institution_longitude !== null}
        <p class="mt-1 text-xs text-ink-500">
          {request.institution_latitude}, {request.institution_longitude}
        </p>
      {/if}
    </div>
  {/if}

  {#if request.rejection_reason}
    <p class="rounded-2xl bg-accent-50 p-3 text-sm text-accent-800">
      <strong>Motivo:</strong> {request.rejection_reason}
    </p>
  {/if}

  {#if actionable}
    <div class="flex flex-wrap justify-end gap-2">
      <Button variant="danger" size="sm" icon="close" disabled={busy} on:click={() => dispatch('reject', request)}>Recusar</Button>
      <Button size="sm" icon="check" loading={busy} on:click={() => dispatch('approve', request)}>Aprovar</Button>
    </div>
  {/if}
</Card>
