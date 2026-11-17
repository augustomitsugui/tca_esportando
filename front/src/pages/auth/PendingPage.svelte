<script>
  import { onMount } from 'svelte';
  import { session, signOut, refreshUser } from '../../stores/auth.js';
  import { roleRequestService } from '../../services/roleRequestService.js';
  import { errorMessage } from '../../services/api.js';
  import { toast } from '../../stores/toast.js';
  import Card from '../../components/ui/Card.svelte';
  import Icon from '../../components/ui/Icon.svelte';
  import Button from '../../components/ui/Button.svelte';
  import Spinner from '../../components/ui/Spinner.svelte';
  import Alert from '../../components/ui/Alert.svelte';
  import RequestCard from '../../components/features/RequestCard.svelte';

  let request = null;
  let loading = true;
  let checking = false;
  let error = '';

  async function load() {
    loading = true;
    error = '';
    try {
      const list = await roleRequestService.mine();
      request = [...list].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0] ?? null;
    } catch (err) {
      error = errorMessage(err);
    } finally {
      loading = false;
    }
  }

  // Ao atualizar, o roteador libera o painel sozinho se já foi aprovado.
  async function check() {
    checking = true;
    try {
      await refreshUser();
      await load();
      if ($session.user?.approval_status !== 'aprovada') {
        toast.error('Ainda não há novidades na sua solicitação.');
      }
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      checking = false;
    }
  }

  onMount(load);
</script>

<Card class="space-y-5 p-8 text-center">
  <span class="mx-auto grid h-20 w-20 animate-float place-items-center rounded-full bg-brand-100 text-brand-600">
    <Icon name="hourglass_top" size={42} />
  </span>
  <div>
    <h1 class="sport-title text-5xl text-brand-800">Quase lá!</h1>
    <p class="mt-1 text-ink-500">
      Sua conta de {$session.user?.role} precisa ser aprovada antes de você entrar no painel.
    </p>
  </div>

  {#if loading}
    <Spinner />
  {:else if error}
    <Alert message={error} />
  {:else if request}
    <div class="text-left"><RequestCard {request} /></div>
  {/if}

  <div class="flex flex-wrap justify-center gap-3">
    <Button icon="refresh" loading={checking} on:click={check}>Verificar novamente</Button>
    <Button variant="outline" icon="logout" on:click={signOut}>Sair</Button>
  </div>
</Card>
