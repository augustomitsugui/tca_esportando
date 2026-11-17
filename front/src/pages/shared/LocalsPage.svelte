<script>
  import { session } from '../../stores/auth.js';
  import { resources } from '../../config/resources.js';
  import ResourceManager from '../../components/features/ResourceManager.svelte';
  import LocalLinksModal from '../../components/features/LocalLinksModal.svelte';

  export let resource;

  $: config = resources[resource];
  let linking = null;

  const onAction = (event) => {
    if (event.detail.id === 'links') linking = event.detail.item;
  };
</script>

<ResourceManager {config} user={$session.user} on:action={onAction} />

<LocalLinksModal local={linking} sportsEndpoint={config.linksSportsEndpoint} on:close={() => (linking = null)} />
