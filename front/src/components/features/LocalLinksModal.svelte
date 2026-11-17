<script>
  import { createEventDispatcher } from 'svelte';
  import { api, errorMessage } from '../../services/api.js';
  import { localService } from '../../services/localService.js';
  import { toast } from '../../stores/toast.js';
  import Modal from '../ui/Modal.svelte';
  import Spinner from '../ui/Spinner.svelte';
  import Alert from '../ui/Alert.svelte';
  import Button from '../ui/Button.svelte';
  import ToggleRow from './ToggleRow.svelte';

  // Vínculos de um local com esportes e instituições
  export let local = null; // registro do local (abre quando != null)
  export let sportsEndpoint;

  const dispatch = createEventDispatcher();

  let loading = false;
  let error = '';
  let busyKey = '';
  let sports = [];
  let institutions = [];
  let linkedSports = new Set();
  let linkedInstitutions = new Set();

  $: if (local) load(local.id);

  async function load(localId) {
    loading = true;
    error = '';
    try {
      const [allSports, allInstitutions, sportLinks, institutionLinks] = await Promise.all([
        api.get(sportsEndpoint),
        api.get('/instituicoes'),
        localService.sports(localId),
        localService.institutions(localId),
      ]);
      sports = allSports;
      institutions = allInstitutions;
      linkedSports = new Set(sportLinks.map((s) => s.id));
      linkedInstitutions = new Set(institutionLinks.map((i) => i.instituicao_id));
    } catch (err) {
      error = errorMessage(err);
    } finally {
      loading = false;
    }
  }

  async function toggle(kind, id) {
    const isSport = kind === 'sport';
    const set = isSport ? linkedSports : linkedInstitutions;
    const linked = set.has(id);
    busyKey = `${kind}:${id}`;
    try {
      if (isSport) {
        await (linked ? localService.unlinkSport(local.id, id) : localService.linkSport(local.id, id));
      } else {
        await (linked ? localService.unlinkInstitution(local.id, id) : localService.linkInstitution(local.id, id));
      }
      linked ? set.delete(id) : set.add(id);
      if (isSport) linkedSports = new Set(set);
      else linkedInstitutions = new Set(set);
      toast.success(linked ? 'Vínculo removido.' : 'Vínculo criado!');
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      busyKey = '';
    }
  }
</script>

<Modal open={local !== null} title={local ? `Vínculos · ${local.nome}` : ''} icon="link" size="lg" on:close={() => dispatch('close')}>
  {#if loading}
    <Spinner />
  {:else if error}
    <Alert message={error} />
  {:else}
    <h3 class="sport-title mb-2 text-2xl text-brand-800">Esportes</h3>
    <div class="mb-6 space-y-2">
      {#each sports as sport (sport.id)}
        <ToggleRow
          label={sport.nome}
          description={sport.descricao ?? ''}
          linked={linkedSports.has(sport.id)}
          busy={busyKey === `sport:${sport.id}`}
          on:toggle={() => toggle('sport', sport.id)}
        />
      {:else}
        <p class="text-sm text-ink-500">Nenhum esporte disponível.</p>
      {/each}
    </div>

    <h3 class="sport-title mb-2 text-2xl text-brand-800">Instituições</h3>
    <div class="space-y-2">
      {#each institutions as inst (inst.id)}
        <ToggleRow
          label={inst.nome}
          description={inst.descricao ?? ''}
          linked={linkedInstitutions.has(inst.id)}
          busy={busyKey === `institution:${inst.id}`}
          on:toggle={() => toggle('institution', inst.id)}
        />
      {:else}
        <p class="text-sm text-ink-500">Nenhuma instituição disponível.</p>
      {/each}
    </div>
  {/if}

  <svelte:fragment slot="footer">
    <Button variant="outline" on:click={() => dispatch('close')}>Fechar</Button>
  </svelte:fragment>
</Modal>
