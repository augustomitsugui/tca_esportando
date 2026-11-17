<script lang="ts">
  let { texto }: { texto: string } = $props()
</script>

<div
  class="rounded-xl border border-dashed border-slate-300 px-4 py-8 text-center text-sm text-slate-500"
>
  {texto}
</div>
