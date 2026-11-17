import { homePathFor } from '../lib/roles.js';

import AppShell from '../components/layout/AppShell.svelte';
import AuthLayout from '../components/layout/AuthLayout.svelte';

import LoginPage from '../pages/auth/LoginPage.svelte';
import RegisterPage from '../pages/auth/RegisterPage.svelte';
import PendingPage from '../pages/auth/PendingPage.svelte';
import NotFoundPage from '../pages/NotFoundPage.svelte';
import DashboardPage from '../pages/dashboard/DashboardPage.svelte';
import ResourcePage from '../pages/shared/ResourcePage.svelte';
import ProfilePage from '../pages/shared/ProfilePage.svelte';
import LocalsPage from '../pages/shared/LocalsPage.svelte';
import RequestsPage from '../pages/shared/RequestsPage.svelte';
import AthleteSportsPage from '../pages/athlete/AthleteSportsPage.svelte';
import AthleteTrainingsPage from '../pages/athlete/AthleteTrainingsPage.svelte';
import TrainerLinksPage from '../pages/trainer/TrainerLinksPage.svelte';

const app = { access: 'private', layout: AppShell };
const only = (...roles) => ({ ...app, roles });

export const routes = [
  { path: '/', redirect: (user) => homePathFor(user) },

  // --- público ---
  { path: '/login', title: 'Entrar', access: 'guest', layout: AuthLayout, component: LoginPage },
  { path: '/cadastro', title: 'Criar conta', access: 'guest', layout: AuthLayout, component: RegisterPage },

  // --- treinador/coordenador aguardando aprovação ---
  { path: '/aguardando', title: 'Aguardando aprovação', access: 'private', pendingOnly: true, layout: AuthLayout, component: PendingPage },

  // --- painel (atleta, treinador, coordenador) ---
  { path: '/painel', title: 'Início', ...only('atleta', 'treinador', 'coordenador'), component: DashboardPage },
  { path: '/perfil', title: 'Meu perfil', ...only('atleta', 'treinador', 'coordenador'), component: ProfilePage, props: { resource: 'perfil' } },

  // --- atleta ---
  { path: '/atleta/esportes', title: 'Esportes', ...only('atleta'), component: AthleteSportsPage },
  { path: '/atleta/treinos', title: 'Meus treinos', ...only('atleta'), component: AthleteTrainingsPage },

  // --- treinador ---
  { path: '/treinador/esportes', title: 'Meus esportes', ...only('treinador'), component: ResourcePage, props: { resource: 'treinadorEsportes' } },
  { path: '/treinador/locais', title: 'Locais', ...only('treinador'), component: ResourcePage, props: { resource: 'treinadorLocais' } },
  { path: '/treinador/treinos', title: 'Treinos', ...only('treinador'), component: ResourcePage, props: { resource: 'treinadorTreinos' } },
  { path: '/treinador/solicitacoes', title: 'Pedidos de atletas', ...only('treinador'), component: TrainerLinksPage, props: { mode: 'pending' } },
  { path: '/treinador/atletas', title: 'Meus atletas', ...only('treinador'), component: TrainerLinksPage, props: { mode: 'approved' } },

  // --- coordenador ---
  { path: '/coordenador/instituicao', title: 'Instituição', ...only('coordenador'), component: ProfilePage, props: { resource: 'coordenadorInstituicao' } },
  { path: '/coordenador/locais', title: 'Locais', ...only('coordenador'), component: LocalsPage, props: { resource: 'coordenadorLocais' } },
  { path: '/coordenador/esportes', title: 'Esportes', ...only('coordenador'), component: ResourcePage, props: { resource: 'coordenadorEsportes' } },
  { path: '/coordenador/solicitacoes', title: 'Pedidos de treinadores', ...only('coordenador'), component: RequestsPage, props: { mode: 'coordenador' } },

  // --- administrador ---
  { path: '/admin', title: 'Administração', ...only('admin'), component: DashboardPage },
  { path: '/admin/solicitacoes', title: 'Solicitações', ...only('admin'), component: RequestsPage, props: { mode: 'admin' } },
  { path: '/admin/instituicoes', title: 'Instituições', ...only('admin'), component: ResourcePage, props: { resource: 'adminInstituicoes' } },
  { path: '/admin/coordenadores', title: 'Coordenadores', ...only('admin'), component: ResourcePage, props: { resource: 'adminCoordenadores' } },
  { path: '/admin/treinadores', title: 'Treinadores', ...only('admin'), component: ResourcePage, props: { resource: 'adminTreinadores' } },
  { path: '/admin/atletas', title: 'Atletas', ...only('admin'), component: ResourcePage, props: { resource: 'adminAtletas' } },
  { path: '/admin/esportes', title: 'Esportes', ...only('admin'), component: ResourcePage, props: { resource: 'adminEsportes' } },
  { path: '/admin/locais', title: 'Locais', ...only('admin'), component: LocalsPage, props: { resource: 'adminLocais' } },
  { path: '/admin/treinos', title: 'Treinos', ...only('admin'), component: ResourcePage, props: { resource: 'adminTreinos' } },
];

export const notFoundRoute = {
  path: '*',
  title: 'Página não encontrada',
  access: 'public',
  layout: AuthLayout,
  component: NotFoundPage,
};
