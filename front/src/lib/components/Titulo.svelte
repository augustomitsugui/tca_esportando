<script lang="ts">
  import type { Snippet } from 'svelte'

  let {
    titulo,
    subtitulo = '',
    children,
  }: { titulo: string; subtitulo?: string; children?: Snippet } = $props()
</script>

<div class="mb-6 flex flex-wrap items-end justify-between gap-3">
  <div>
    <h1 class="text-2xl font-bold text-slate-900">{titulo}</h1>
    {#if subtitulo}
      <p class="mt-1 text-sm text-slate-500">{subtitulo}</p>
    {/if}
  </div>
  {#if children}
    <div class="flex flex-wrap gap-2">{@render children()}</div>
  {/if}
</div>
