<script>
  import { onMount } from 'svelte';
  import { session } from '../../stores/auth.js';
  import { api, errorMessage } from '../../services/api.js';
  import { singles } from '../../config/resources.js';
  import { valuesFromRecord, toPayload } from '../../lib/fields.js';
  import { toast } from '../../stores/toast.js';
  import PageHeader from '../../components/ui/PageHeader.svelte';
  import Card from '../../components/ui/Card.svelte';
  import Button from '../../components/ui/Button.svelte';
  import Spinner from '../../components/ui/Spinner.svelte';
  import Alert from '../../components/ui/Alert.svelte';
  import EmptyState from '../../components/ui/EmptyState.svelte';
  import DynamicForm from '../../components/forms/DynamicForm.svelte';

  // Edição de um único registro (perfil do usuário, instituição do coordenador)
  export let resource;

  const config = singles[resource]($session.user);

  let values = {};
  let loading = true;
  let saving = false;
  let error = '';

  onMount(async () => {
    try {
      const record = await api.get(config.endpoint);
      values = valuesFromRecord(config.fields, record);
    } catch (err) {
      error = errorMessage(err);
    } finally {
      loading = false;
    }
  });

  async function save() {
    saving = true;
    error = '';
    try {
      await api.put(config.endpoint, toPayload(config.fields, values));
      toast.success('Dados atualizados!');
    } catch (err) {
      error = errorMessage(err);
    } finally {
      saving = false;
    }
  }
</script>

<PageHeader title={config.title} subtitle={config.subtitle} icon={config.icon} />

<Card class="max-w-2xl">
  {#if loading}
    <Spinner />
  {:else if !Object.keys(values).length}
    <Alert message={error} />
    <EmptyState title="Não foi possível carregar" />
  {:else}
    <form class="space-y-4" on:submit|preventDefault={save}>
      <Alert message={error} />
      <DynamicForm fields={config.fields} bind:values />
      <div class="flex justify-end">
        <Button type="submit" icon="check" loading={saving}>Salvar</Button>
      </div>
    </form>
  {/if}
</Card>
