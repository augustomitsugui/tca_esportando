<script>
  import Link from '../../router/Link.svelte';
  import { navigate } from '../../router/router.js';
  import { signIn } from '../../stores/auth.js';
  import { authService } from '../../services/authService.js';
  import { errorMessage } from '../../services/api.js';
  import { toast } from '../../stores/toast.js';
  import { homePathFor } from '../../lib/roles.js';
  import Card from '../../components/ui/Card.svelte';
  import Alert from '../../components/ui/Alert.svelte';
  import RoleSelector from '../../components/forms/RoleSelector.svelte';
  import RegisterForm from '../../components/forms/RegisterForm.svelte';

  let role = 'atleta';
  let loading = false;
  let error = '';

  async function register(event) {
    const payload = event.detail;
    loading = true;
    error = '';
    try {
      await authService.register(role, payload);
      const user = await signIn(payload.email, payload.password);
      toast.success('Conta criada! Bem-vindo ao Esportando.');
      navigate(homePathFor(user), { replace: true });
    } catch (err) {
      error = errorMessage(err);
      loading = false;
    }
  }
</script>

<Card class="p-8">
  <h1 class="sport-title text-5xl text-brand-800">Entre para o time</h1>
  <p class="mb-5 mt-1 text-ink-500">Escolha como você vai usar o Esportando.</p>

  <RoleSelector bind:value={role} />

  <div class="mt-6 space-y-4">
    <Alert message={error} />
    {#key role}
      <RegisterForm {role} {loading} on:submit={register} />
    {/key}
  </div>

  <p class="mt-6 text-center text-ink-500">
    Já tem conta?
    <Link to="/login" class="font-bold text-accent-600 hover:underline">Entrar</Link>
  </p>
</Card>
