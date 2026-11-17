<script>
  import Icon from './Icon.svelte';

  export let variant = 'primary'; // primary | accent | outline | danger | ghost
  export let size = 'md'; // sm | md
  export let type = 'button';
  export let icon = '';
  export let loading = false;
  export let disabled = false;
  export let full = false;

  const variants = {
    primary: 'bg-brand-600 text-white shadow-soft hover:bg-brand-700',
    accent: 'bg-accent-600 text-white shadow-soft hover:bg-accent-700',
    outline: 'border-2 border-brand-200 bg-white text-brand-700 hover:bg-brand-50',
    danger: 'bg-accent-50 text-accent-700 hover:bg-accent-100',
    ghost: 'text-ink-600 hover:bg-brand-50',
  };
  const sizes = {
    sm: 'px-4 py-1.5 text-sm',
    md: 'px-6 py-2.5 text-base',
  };
</script>

<button
  {type}
  disabled={disabled || loading}
  on:click
  class="inline-flex items-center justify-center gap-2 rounded-full font-display font-bold uppercase tracking-wider transition active:scale-95 disabled:pointer-events-none disabled:opacity-50 {variants[variant]} {sizes[size]} {full ? 'w-full' : ''}"
>
  {#if loading}
    <Icon name="progress_activity" size={20} class="animate-spin" />
  {:else if icon}
    <Icon name={icon} size={size === 'sm' ? 18 : 22} />
  {/if}
  <slot />
</button>
