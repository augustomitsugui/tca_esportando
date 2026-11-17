# Esportando - Frontend

Svelte 4 + Vite + Tailwind. Roteamento por caminho (History API), sem `#`.

## Como rodar

1. Suba o backend (pasta `back`): `docker compose up -d --build` e depois `docker compose exec web python -m alembic upgrade head`.
2. Na pasta `front`: `docker compose up --build`.
3. Abra http://localhost:5173

O navegador chama `/api/...` e o Vite repassa para o backend (`BACKEND_URL` no `docker-compose.yml`), por isso não é preciso mexer em CORS.

## Perfil administrador

O backend não possui rota para criar admin. Para acessar `/admin`, marque o usuário como superusuário no banco:

```sql
UPDATE "user" SET is_superuser = true WHERE email = 'seu@email.com';
```

(ajuste o nome da tabela se o seu modelo usar outro nome).

## Estrutura

```
src/
  App.svelte            raiz: carrega a sessão e monta o roteador
  router/               roteador por path, guards, rotas e Link
  components/
    ui/                 botões, campos, cards, modal, tabela, badges...
    layout/             AppShell, Sidebar, Topbar, AuthLayout
    forms/              formulário de cadastro e seletor de perfil
    features/           ResourceManager (CRUD genérico), cards de domínio
  pages/                páginas (finas, só compõem componentes)
  services/             acesso à API (uma responsabilidade por arquivo)
  stores/               sessão e toasts
  config/               navegação, recursos e dashboards
```

Regras de negócio ficam no backend: o front apenas envia os dados e mostra a resposta/erro da API.
