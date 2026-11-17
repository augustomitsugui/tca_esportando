<script>
  import Link from '../../router/Link.svelte';
  import { navigate } from '../../router/router.js';
  import { signIn } from '../../stores/auth.js';
  import { errorMessage } from '../../services/api.js';
  import { homePathFor } from '../../lib/roles.js';
  import Card from '../../components/ui/Card.svelte';
  import TextField from '../../components/ui/TextField.svelte';
  import Button from '../../components/ui/Button.svelte';
  import Alert from '../../components/ui/Alert.svelte';

  let email = '';
  let password = '';
  let loading = false;
  let error = '';

  async function submit() {
    loading = true;
    error = '';
    try {
      const user = await signIn(email, password);
      navigate(homePathFor(user), { replace: true });
    } catch (err) {
      error = errorMessage(err);
      loading = false;
    }
  }
</script>

<Card class="p-8">
  <h1 class="sport-title text-5xl text-brand-800">Bem-vindo de volta</h1>
  <p class="mb-6 mt-1 text-ink-500">Entre para ver seus esportes e treinos.</p>

  <form class="space-y-4" on:submit|preventDefault={submit}>
    <Alert message={error} />
    <TextField label="E-mail" name="email" type="email" icon="mail" bind:value={email} required autocomplete="email" />
    <TextField label="Senha" name="password" type="password" icon="lock" bind:value={password} required autocomplete="current-password" />
    <Button type="submit" full {loading} icon="login">Entrar</Button>
  </form>

  <p class="mt-6 text-center text-ink-500">
    Ainda não tem conta?
    <Link to="/cadastro" class="font-bold text-accent-600 hover:underline">Criar conta</Link>
  </p>
</Card>
