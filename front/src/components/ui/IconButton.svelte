<script>
  import Icon from './Icon.svelte';

  export let icon;
  export let title;
  export let tone = 'neutral'; // neutral | danger
  export let disabled = false;

  const tones = {
    neutral: 'text-brand-700 hover:bg-brand-100',
    danger: 'text-accent-600 hover:bg-accent-100',
  };
</script>

<button
  type="button"
  {title}
  aria-label={title}
  {disabled}
  on:click
  class="grid h-9 w-9 place-items-center rounded-full transition active:scale-90 disabled:opacity-40 {tones[tone]}"
>
  <Icon name={icon} size={20} />
</button>
