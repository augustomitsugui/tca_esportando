<script>
  import { onMount } from 'svelte';
  import SelectField from '../ui/SelectField.svelte';
  import { authService } from '../../services/authService.js';

  export let value = '';
  export let required = true;

  let options = [];
  let hint = 'Carregando instituições...';

  onMount(async () => {
    try {
      const list = await authService.publicInstitutions();
      options = list.map((i) => ({ value: i.id, label: i.nome }));
      hint = options.length ? '' : 'Nenhuma instituição cadastrada ainda.';
    } catch {
      hint = 'Não foi possível carregar as instituições.';
    }
  });
</script>

<SelectField
  label="Instituição"
  name="institution_id"
  bind:value
  {options}
  {required}
  {hint}
  placeholder="Escolha a sua instituição"
/>
