<script lang="ts">
  let { texto = 'Carregando...' }: { texto?: string } = $props()
</script>

<div class="flex items-center justify-center gap-3 py-10 text-slate-500" role="status">
  <span
    class="h-5 w-5 animate-spin rounded-full border-2 border-emerald-600 border-t-transparent"
  ></span>
  <span class="text-sm">{texto}</span>
</div>
