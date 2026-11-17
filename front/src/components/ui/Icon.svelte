<script>
  // Ícones Material Symbols (Google)
  export let name;
  export let size = 24;
  export let filled = false;
  let className = '';
  export { className as class };
</script>

<span
  class="material-symbols-rounded select-none leading-none {className}"
  style="font-size:{size}px;font-variation-settings:'FILL' {filled ? 1 : 0}, 'wght' 500, 'GRAD' 0, 'opsz' 24;"
  aria-hidden="true">{name}</span
>
