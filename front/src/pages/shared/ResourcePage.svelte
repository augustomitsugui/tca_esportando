<script>
  import { session } from '../../stores/auth.js';
  import { resources } from '../../config/resources.js';
  import ResourceManager from '../../components/features/ResourceManager.svelte';

  export let resource;
</script>

<ResourceManager config={resources[resource]} user={$session.user} />
