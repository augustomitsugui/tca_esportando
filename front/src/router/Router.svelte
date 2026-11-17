<script>
  import { location, navigate, matchRoute } from './router.js';
  import { routes, notFoundRoute } from './routes.js';
  import { resolveGuard } from './guards.js';
  import { session } from '../stores/auth.js';

  $: route = matchRoute(routes, $location.path) ?? notFoundRoute;
  $: redirect = resolveGuard(route, $session.user);
  $: if (redirect && redirect !== $location.path) {
    navigate(redirect, { replace: true });
  }
  $: if (!redirect) {
    document.title = route.title ? `${route.title} · Esportando` : 'Esportando';
  }
</script>

{#if !redirect}
  {#key $location.path}
    {#if route.layout}
      <svelte:component this={route.layout}>
        <svelte:component this={route.component} {...route.props ?? {}} />
      </svelte:component>
    {:else}
      <svelte:component this={route.component} {...route.props ?? {}} />
    {/if}
  {/key}
{/if}
