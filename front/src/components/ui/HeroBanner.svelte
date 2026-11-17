<script>
  import Icon from './Icon.svelte';

  export let title;
  export let subtitle = '';
  export let icon = 'sports_soccer';
</script>

<section class="stripes relative overflow-hidden rounded-3xl bg-gradient-to-br from-brand-600 to-brand-800 p-6 text-white shadow-lift sm:p-8">
  <span class="absolute -right-10 -top-10 h-48 w-24 rotate-[28deg] bg-accent-600/90"></span>
  <span class="absolute -right-2 -top-10 h-48 w-6 rotate-[28deg] bg-white/90"></span>
  <Icon name={icon} size={120} filled class="absolute -bottom-6 right-20 hidden animate-float text-white/15 sm:block" />
  <div class="relative max-w-xl">
    <h1 class="sport-title text-4xl text-white sm:text-5xl">{title}</h1>
    {#if subtitle}<p class="mt-2 text-lg text-brand-100">{subtitle}</p>{/if}
  </div>
</section>
