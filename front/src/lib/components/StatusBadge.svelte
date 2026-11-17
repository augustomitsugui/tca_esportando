<script lang="ts">
  let { status }: { status: string } = $props()

  const estilos: Record<string, string> = {
    pendente: 'bg-amber-100 text-amber-800',
    aprovada: 'bg-emerald-100 text-emerald-800',
    aprovado: 'bg-emerald-100 text-emerald-800',
    rejeitada: 'bg-red-100 text-red-800',
    recusado: 'bg-red-100 text-red-800',
  }
</script>

<span
  class="inline-block rounded-full px-2.5 py-0.5 text-xs font-semibold capitalize {estilos[status] ??
    'bg-slate-100 text-slate-700'}"
>
  {status}
</span>
