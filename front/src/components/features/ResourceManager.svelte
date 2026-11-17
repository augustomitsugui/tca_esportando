<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { api, errorMessage } from '../../services/api.js';
  import { toast } from '../../stores/toast.js';
  import { emptyValues, valuesFromRecord, toPayload } from '../../lib/fields.js';
  import { formatDateTime } from '../../lib/format.js';

  import PageHeader from '../ui/PageHeader.svelte';
  import Card from '../ui/Card.svelte';
  import Button from '../ui/Button.svelte';
  import IconButton from '../ui/IconButton.svelte';
  import DataTable from '../ui/DataTable.svelte';
  import Spinner from '../ui/Spinner.svelte';
  import EmptyState from '../ui/EmptyState.svelte';
  import Alert from '../ui/Alert.svelte';
  import Modal from '../ui/Modal.svelte';
  import ConfirmDialog from '../ui/ConfirmDialog.svelte';
  import DynamicForm from '../forms/DynamicForm.svelte';

  // CRUD genérico: o backend decide o que é permitido, aqui só mostramos o resultado.
  export let config;
  export let user = null;

  const dispatch = createEventDispatcher();

  let items = [];
  let options = {};
  let loading = true;
  let loadError = '';

  let formOpen = false;
  let editing = null;
  let values = {};
  let formError = '';
  let saving = false;

  let toDelete = null;
  let deleting = false;

  $: editable = config.edit === true;
  $: removable = config.remove === true;
  $: hasRowActions = editable || removable || (config.actions?.length ?? 0) > 0;
  $: formFields = config.fields.filter((f) => !f.only || (f.only === 'create' && !editing));

  $: columns = config.columns.map((col) => ({
    ...col,
    render: (row) => {
      if (col.lookup) {
        const found = (options[col.lookup] ?? []).find((o) => o.value === row[col.key]);
        return found ? found.label : row[col.key] ? 'Item removido' : '—';
      }
      if (col.type === 'datetime') return formatDateTime(row[col.key]);
      return row[col.key];
    },
  }));

  async function loadOptions() {
    const selects = config.fields.filter((f) => f.optionsFrom);
    const loaded = await Promise.all(
      selects.map(async (f) => {
        const { endpoint, value, label } = f.optionsFrom;
        const list = await api.get(endpoint).catch(() => []);
        return [f.key, list.map((item) => ({ value: item[value], label: item[label] }))];
      }),
    );
    options = Object.fromEntries(loaded);
  }

  async function load() {
    loading = true;
    loadError = '';
    try {
      const [list] = await Promise.all([api.get(config.endpoint), loadOptions()]);
      items = list;
    } catch (err) {
      loadError = errorMessage(err);
    } finally {
      loading = false;
    }
  }

  onMount(load);

  function openCreate() {
    editing = null;
    values = emptyValues(config.fields);
    formError = '';
    formOpen = true;
  }

  function openEdit(item) {
    editing = item;
    values = valuesFromRecord(config.fields, item);
    formError = '';
    formOpen = true;
  }

  async function save() {
    saving = true;
    formError = '';
    try {
      const payload = toPayload(formFields, values);
      if (editing) {
        await api.put(`${config.endpoint}/${editing.id}`, payload);
        toast.success(`Salvo com sucesso.`);
      } else {
        await api.post(config.endpoint, { ...payload, ...(config.defaults?.(user) ?? {}) });
        toast.success(`Novo(a) ${config.singular} criado(a)!`);
      }
      formOpen = false;
      await load();
    } catch (err) {
      formError = errorMessage(err);
    } finally {
      saving = false;
    }
  }

  async function confirmDelete() {
    deleting = true;
    try {
      await api.del(`${config.endpoint}/${toDelete.id}`);
      toast.success('Removido com sucesso.');
      toDelete = null;
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
      toDelete = null;
    } finally {
      deleting = false;
    }
  }
</script>

<PageHeader title={config.title} subtitle={config.subtitle} icon={config.icon}>
  {#if config.create}
    <Button icon="add" on:click={openCreate}>Novo {config.singular}</Button>
  {/if}
</PageHeader>

<Card padded={false} class="overflow-hidden">
  {#if loading}
    <Spinner />
  {:else if loadError}
    <div class="p-6">
      <Alert message={loadError} />
      <div class="mt-4"><Button variant="outline" icon="refresh" on:click={load}>Tentar de novo</Button></div>
    </div>
  {:else if items.length === 0}
    <EmptyState title="Nenhum registro" text={`Ainda não há ${config.singular} por aqui.`}>
      {#if config.create}
        <Button icon="add" on:click={openCreate}>Criar o primeiro</Button>
      {/if}
    </EmptyState>
  {:else}
    <DataTable {columns} rows={items}>
      <svelte:fragment slot="actions" let:row>
        {#if hasRowActions}
          {#each config.actions ?? [] as action}
            <IconButton icon={action.icon} title={action.label} on:click={() => dispatch('action', { id: action.id, item: row })} />
          {/each}
          {#if editable}<IconButton icon="edit" title="Editar" on:click={() => openEdit(row)} />{/if}
          {#if removable}<IconButton icon="delete" title="Excluir" tone="danger" on:click={() => (toDelete = row)} />{/if}
        {/if}
      </svelte:fragment>
    </DataTable>
  {/if}
</Card>

<Modal
  open={formOpen}
  title={editing ? `Editar ${config.singular}` : `Novo ${config.singular}`}
  icon={editing ? 'edit' : 'add_circle'}
  on:close={() => (formOpen = false)}
>
  <form id="resource-form" class="space-y-4" on:submit|preventDefault={save}>
    <Alert message={formError} />
    <DynamicForm fields={formFields} bind:values {options} />
  </form>
  <svelte:fragment slot="footer">
    <Button variant="ghost" on:click={() => (formOpen = false)}>Cancelar</Button>
    <Button
      loading={saving}
      icon="check"
      on:click={() => document.getElementById('resource-form')?.requestSubmit()}
    >
      Salvar
    </Button>
  </svelte:fragment>
</Modal>

<ConfirmDialog
  open={toDelete !== null}
  title={`Excluir ${config.singular}?`}
  message="Essa ação não pode ser desfeita."
  confirmLabel="Excluir"
  loading={deleting}
  on:cancel={() => (toDelete = null)}
  on:confirm={confirmDelete}
/>
