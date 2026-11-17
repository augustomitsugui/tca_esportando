<script>
  import { onMount } from 'svelte';
  import { session } from '../../stores/auth.js';
  import { getRole } from '../../lib/roles.js';
  import { displayName } from '../../lib/format.js';
  import { dashboards } from '../../config/dashboards.js';
  import { navigation } from '../../config/navigation.js';
  import HeroBanner from '../../components/ui/HeroBanner.svelte';
  import StatCard from '../../components/ui/StatCard.svelte';
  import QuickLink from '../../components/features/QuickLink.svelte';
  import UpcomingTreinos from './UpcomingTreinos.svelte';

  $: user = $session.user;
  $: role = getRole(user);
  $: config = dashboards[role];
  $: shortcuts = (navigation[role] ?? []).filter((item) => !item.exact && item.hint);

  let values = [];

  // cada contador carrega sozinho; se um falhar, mostra "—"
  async function loadStats() {
    values = config.stats.map(() => null);
    await Promise.all(
      config.stats.map(async (stat, i) => {
        try {
          const result = await stat.load(user);
          values[i] = result;
        } catch {
          values[i] = null;
        }
        values = values;
      }),
    );
  }

  onMount(loadStats);
</script>

{#if config}
  <div class="space-y-8">
    <HeroBanner
      title={role === 'admin' ? 'Painel do administrador' : `Fala, ${displayName(user)}!`}
      subtitle={config.subtitle}
      icon={config.icon}
    />

    <section class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {#each config.stats as stat, i}
        <StatCard label={stat.label} icon={stat.icon} tone={stat.tone} value={values[i]} />
      {/each}
    </section>

    {#if role === 'atleta' && user.profile_id}
      <UpcomingTreinos atletaId={user.profile_id} />
    {/if}

    <section>
      <h2 class="sport-title mb-3 text-3xl text-brand-800">Atalhos</h2>
      <div class="grid gap-4 md:grid-cols-2">
        {#each shortcuts as item}
          <QuickLink to={item.to} icon={item.icon} title={item.label} text={item.hint} />
        {/each}
      </div>
    </section>
  </div>
{/if}
