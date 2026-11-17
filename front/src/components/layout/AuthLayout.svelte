<script>
  import Logo from '../ui/Logo.svelte';
  import Icon from '../ui/Icon.svelte';

  const floating = [
    { icon: 'sports_soccer', pos: 'left-[10%] top-[14%]', size: 64, delay: '0s' },
    { icon: 'sports_basketball', pos: 'right-[12%] top-[26%]', size: 56, delay: '1.2s' },
    { icon: 'sports_volleyball', pos: 'left-[18%] bottom-[22%]', size: 60, delay: '2.4s' },
    { icon: 'directions_run', pos: 'right-[16%] bottom-[14%]', size: 56, delay: '3.2s' },
    { icon: 'emoji_events', pos: 'left-[46%] top-[8%]', size: 48, delay: '0.6s' },
  ];
</script>

<div class="grid min-h-screen lg:grid-cols-[1.05fr_1fr]">
  <!-- painel esportivo -->
  <section class="stripes relative hidden overflow-hidden bg-gradient-to-br from-brand-600 via-brand-700 to-brand-900 lg:block">
    <span class="absolute -right-24 top-0 h-[140%] w-40 rotate-[18deg] bg-accent-600"></span>
    <span class="absolute -right-4 top-0 h-[140%] w-8 rotate-[18deg] bg-white/90"></span>

    {#each floating as f}
      <Icon
        name={f.icon}
        size={f.size}
        filled
        class="absolute animate-float text-white/25 {f.pos}"
      />
    {/each}

    <div class="relative flex h-full flex-col justify-between p-12 text-white">
      <Logo light />
      <div>
        <h2 class="sport-title text-7xl leading-[0.9] text-white xl:text-8xl">
          Vamos<br />jogar<br />juntos
        </h2>
        <p class="mt-5 max-w-sm text-lg text-brand-100">
          Esportes, treinos e atletas num só lugar.
        </p>
      </div>
      <p class="text-sm text-brand-200">Esportando</p>
    </div>
  </section>

  <!-- conteúdo -->
  <main class="flex items-center justify-center px-4 py-10 sm:px-10">
    <div class="w-full max-w-xl">
      <div class="mb-8 lg:hidden"><Logo /></div>
      <slot />
    </div>
  </main>
</div>
