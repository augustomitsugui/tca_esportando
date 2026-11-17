<script>
  import { createEventDispatcher } from 'svelte';
  import Modal from './Modal.svelte';
  import Button from './Button.svelte';
  import TextArea from './TextArea.svelte';

  export let open = false;
  export let title = 'Tem certeza?';
  export let message = '';
  export let confirmLabel = 'Confirmar';
  export let tone = 'danger'; // danger | primary
  export let loading = false;
  export let askReason = false; // pede um motivo (ex.: recusar solicitação)
  export let reasonLabel = 'Motivo';
  export let reason = '';

  const dispatch = createEventDispatcher();
</script>

<Modal {open} {title} icon={tone === 'danger' ? 'warning' : 'help'} size="sm" on:close={() => dispatch('cancel')}>
  {#if message}<p class="mb-4 text-ink-600">{message}</p>{/if}
  {#if askReason}
    <TextArea label={reasonLabel} name="reason" bind:value={reason} required />
  {/if}

  <svelte:fragment slot="footer">
    <Button variant="ghost" on:click={() => dispatch('cancel')}>Cancelar</Button>
    <Button
      variant={tone === 'danger' ? 'accent' : 'primary'}
      {loading}
      disabled={askReason && !reason.trim()}
      on:click={() => dispatch('confirm')}
    >
      {confirmLabel}
    </Button>
  </svelte:fragment>
</Modal>
