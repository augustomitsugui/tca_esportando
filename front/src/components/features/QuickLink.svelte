<script>
  import Link from '../../router/Link.svelte';
  import Card from '../ui/Card.svelte';
  import Icon from '../ui/Icon.svelte';

  export let to;
  export let icon;
  export let title;
  export let text = '';
</script>

<Link {to} class="block">
  <Card hover class="flex h-full items-center gap-4">
    <span class="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-accent-100 text-accent-600">
      <Icon name={icon} size={26} />
    </span>
    <div class="min-w-0 flex-1">
      <h3 class="sport-title text-2xl text-brand-800">{title}</h3>
      {#if text}<p class="text-sm text-ink-500">{text}</p>{/if}
    </div>
    <Icon name="arrow_forward" class="text-brand-400" />
  </Card>
</Link>
