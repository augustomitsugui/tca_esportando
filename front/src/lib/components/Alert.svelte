<script lang="ts">
  let {
    tipo = 'erro',
    mensagem = '',
  }: { tipo?: 'erro' | 'sucesso' | 'info'; mensagem?: string } = $props()

  const estilos = {
    erro: 'border-red-200 bg-red-50 text-red-800',
    sucesso: 'border-emerald-200 bg-emerald-50 text-emerald-800',
    info: 'border-sky-200 bg-sky-50 text-sky-800',
  }
</script>

{#if mensagem}
  <div
    role={tipo === 'erro' ? 'alert' : 'status'}
    class="rounded-lg border px-4 py-3 text-sm {estilos[tipo]}"
  >
    {mensagem}
  </div>
{/if}
