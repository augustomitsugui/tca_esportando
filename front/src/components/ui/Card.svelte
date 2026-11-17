<script>
  export let padded = true;
  export let hover = false;
  let className = '';
  export { className as class };
</script>

<div
  class="rounded-3xl border border-brand-100 bg-white shadow-soft {padded ? 'p-6' : ''} {hover
    ? 'transition hover:-translate-y-1 hover:shadow-lift'
    : ''} {className}"
>
  <slot />
</div>
