<script>
  import { onMount } from 'svelte';
  import Router from './router/Router.svelte';
  import ToastHost from './components/ui/ToastHost.svelte';
  import Spinner from './components/ui/Spinner.svelte';
  import { session, bootstrap } from './stores/auth.js';

  onMount(bootstrap);
</script>

{#if $session.ready}
  <Router />
{:else}
  <div class="grid min-h-screen place-items-center">
    <Spinner label="Aquecendo os motores..." />
  </div>
{/if}

<ToastHost />
