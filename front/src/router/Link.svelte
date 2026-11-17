<script>
  import { createEventDispatcher } from 'svelte';
  import { navigate } from './router.js';

  export let to;
  export let replace = false;
  let className = '';
  export { className as class };

  const dispatch = createEventDispatcher();

  function onClick(event) {
    const modified =
      event.metaKey || event.ctrlKey || event.shiftKey || event.altKey;
    if (event.defaultPrevented || event.button !== 0 || modified) return;
    event.preventDefault();
    navigate(to, { replace });
    dispatch('navigate');
  }
</script>

<a href={to} class={className} on:click={onClick}><slot /></a>
