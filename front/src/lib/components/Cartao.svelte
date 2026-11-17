<script lang="ts">
  import type { Snippet } from 'svelte'

  let { titulo = '', children }: { titulo?: string; children?: Snippet } = $props()
</script>

<section class="cartao">
  {#if titulo}
    <h2 class="mb-4 text-lg font-semibold text-slate-900">{titulo}</h2>
  {/if}
  {@render children?.()}
</section>
