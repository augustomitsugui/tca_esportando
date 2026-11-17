<script>
  import Badge from './Badge.svelte';

  // status vindos do backend: pendente | aprovada | aprovado | rejeitada | recusado
  export let status = '';

  const map = {
    pendente: { tone: 'amber', icon: 'hourglass_top', label: 'Pendente' },
    aprovada: { tone: 'green', icon: 'check_circle', label: 'Aprovada' },
    aprovado: { tone: 'green', icon: 'check_circle', label: 'Aprovado' },
    rejeitada: { tone: 'red', icon: 'cancel', label: 'Rejeitada' },
    recusado: { tone: 'red', icon: 'cancel', label: 'Recusado' },
  };

  $: info = map[status] ?? { tone: 'gray', icon: 'help', label: status || '—' };
</script>

<Badge tone={info.tone} icon={info.icon}>{info.label}</Badge>
