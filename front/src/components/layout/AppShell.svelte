<script>
  import Sidebar from './Sidebar.svelte';
  import Topbar from './Topbar.svelte';
  import { session, signOut } from '../../stores/auth.js';
  import { navigation } from '../../config/navigation.js';
  import { getRole } from '../../lib/roles.js';

  let menuOpen = false;

  $: user = $session.user;
  $: items = navigation[getRole(user)] ?? [];
</script>

{#if user}
  <div class="min-h-screen lg:pl-72">
    <Sidebar {items} open={menuOpen} on:close={() => (menuOpen = false)} />
    <Topbar {user} on:menu={() => (menuOpen = true)} on:logout={signOut} />
    <main class="mx-auto max-w-6xl px-4 py-6 sm:px-8 sm:py-8">
      <slot />
    </main>
  </div>
{/if}
