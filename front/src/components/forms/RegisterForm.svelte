<script>
  import { createEventDispatcher } from 'svelte';
  import TextField from '../ui/TextField.svelte';
  import TextArea from '../ui/TextArea.svelte';
  import Button from '../ui/Button.svelte';
  import InstitutionSelect from './InstitutionSelect.svelte';

  export let role = 'atleta';
  export let loading = false;

  const dispatch = createEventDispatcher();

  let nome = '';
  let email = '';
  let password = '';
  let bio = '';
  let ano = '';
  let institutionId = '';
  let institutionName = '';
  let institutionDescription = '';
  let latitude = '';
  let longitude = '';

  const optional = (v) => (v.trim() === '' ? null : v.trim());
  const optionalNumber = (v) => (String(v).trim() === '' ? null : Number(v));

  function submit() {
    const base = { email, password, nome, bio: optional(bio) };

    if (role === 'atleta') {
      dispatch('submit', { ...base, ano: Number(ano) });
    } else if (role === 'treinador') {
      dispatch('submit', { ...base, institution_id: institutionId });
    } else {
      dispatch('submit', {
        ...base,
        institution_name: institutionName,
        institution_description: optional(institutionDescription),
        institution_latitude: optionalNumber(latitude),
        institution_longitude: optionalNumber(longitude),
      });
    }
  }
</script>

<form class="space-y-4" on:submit|preventDefault={submit}>
  <TextField label="Nome" name="nome" icon="badge" bind:value={nome} maxlength={100} required autocomplete="name" />
  <div class="grid gap-4 sm:grid-cols-2">
    <TextField label="E-mail" name="email" type="email" icon="mail" bind:value={email} required autocomplete="email" />
    <TextField label="Senha" name="password" type="password" icon="lock" bind:value={password} minlength={8} required autocomplete="new-password" hint="Mínimo de 8 caracteres." />
  </div>

  {#if role === 'atleta'}
    <TextField label="Ano" name="ano" type="number" icon="calendar_month" bind:value={ano} required />
  {:else if role === 'treinador'}
    <InstitutionSelect bind:value={institutionId} />
  {:else}
    <div class="space-y-4 rounded-3xl border-2 border-dashed border-brand-200 bg-brand-50/60 p-4">
      <p class="sport-title text-xl text-brand-800">Sua instituição</p>
      <TextField label="Nome da instituição" name="institution_name" icon="account_balance" bind:value={institutionName} maxlength={100} required />
      <TextArea label="Descrição" name="institution_description" bind:value={institutionDescription} maxlength={1024} />
      <div class="grid gap-4 sm:grid-cols-2">
        <TextField label="Latitude" name="institution_latitude" type="number" step="any" bind:value={latitude} />
        <TextField label="Longitude" name="institution_longitude" type="number" step="any" bind:value={longitude} />
      </div>
    </div>
  {/if}

  <TextArea label="Sobre você" name="bio" bind:value={bio} maxlength={1024} />

  <Button type="submit" full {loading} icon="rocket_launch">Criar minha conta</Button>
</form>
