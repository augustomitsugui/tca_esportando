<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from '../ui/Icon.svelte';
  import Avatar from '../ui/Avatar.svelte';
  import Badge from '../ui/Badge.svelte';
  import { ROLE_LABELS, getRole } from '../../lib/roles.js';

  export let user;

  const dispatch = createEventDispatcher();
  $: role = getRole(user);
</script>

<header class="sticky top-0 z-20 flex items-center gap-3 border-b border-brand-100 bg-white/85 px-4 py-3 backdrop-blur sm:px-8">
  <button
    type="button"
    aria-label="Abrir menu"
    class="grid h-10 w-10 place-items-center rounded-full text-brand-700 transition hover:bg-brand-50 lg:hidden"
    on:click={() => dispatch('menu')}
  >
    <Icon name="menu" size={26} />
  </button>

  <div class="flex-1"></div>

  <div class="flex items-center gap-3">
    <div class="hidden text-right sm:block">
      <p class="max-w-[14rem] truncate text-sm font-bold text-ink-900">{user.email}</p>
      <Badge tone={role === 'admin' ? 'red' : 'green'} icon={role === 'admin' ? 'shield_person' : 'verified'}>
        {ROLE_LABELS[role] ?? role}
      </Badge>
    </div>
    <Avatar name={user.email} />
    <button
      type="button"
      title="Sair"
      aria-label="Sair"
      class="grid h-10 w-10 place-items-center rounded-full text-accent-600 transition hover:bg-accent-50"
      on:click={() => dispatch('logout')}
    >
      <Icon name="logout" size={24} />
    </button>
  </div>
</header>
