// Descrição declarativa dos recursos da API.
// O ResourceManager lê estes objetos para montar tabela + formulário.
//
// field.type: text | email | textarea | number | datetime | select
// field.only: 'create' (campo só aparece ao criar)
// field.optionsFrom: { endpoint, value, label } (carrega as opções do select)
// column.lookup: usa as opções de um select para mostrar o nome no lugar do id

const nome = { key: 'nome', label: 'Nome', type: 'text', required: true, maxlength: 100, icon: 'badge' };
const descricao = { key: 'descricao', label: 'Descrição', type: 'textarea', maxlength: 1024 };
const email = { key: 'email', label: 'E-mail', type: 'email', required: true, icon: 'mail' };
const bio = { key: 'bio', label: 'Sobre', type: 'textarea', maxlength: 1024 };

const cols = {
  nome: { key: 'nome', label: 'Nome' },
  descricao: { key: 'descricao', label: 'Descrição' },
  email: { key: 'email', label: 'E-mail' },
  bio: { key: 'bio', label: 'Sobre' },
};

const treinoColumns = [
  cols.nome,
  { key: 'data_hora', label: 'Quando', type: 'datetime' },
  { key: 'esporte_id', label: 'Esporte', lookup: 'esporte_id' },
  { key: 'local_id', label: 'Local', lookup: 'local_id' },
];

const treinoFields = (esportes, locais) => [
  nome,
  descricao,
  { key: 'data_hora', label: 'Data e hora', type: 'datetime', required: true },
  { key: 'esporte_id', label: 'Esporte', type: 'select', required: true, optionsFrom: { endpoint: esportes, value: 'id', label: 'nome' } },
  { key: 'local_id', label: 'Local', type: 'select', required: true, optionsFrom: { endpoint: locais, value: 'id', label: 'nome' } },
];

const esporteFields = [nome, descricao];
const localFields = [nome, descricao];

export const resources = {
  // ---------- treinador ----------
  treinadorEsportes: {
    title: 'Meus esportes',
    subtitle: 'Esportes que você cria e mantém.',
    icon: 'sports_soccer',
    singular: 'esporte',
    endpoint: '/esportes',
    columns: [cols.nome, cols.descricao],
    fields: esporteFields,
    create: true,
    edit: true,
    remove: true,
  },
  treinadorLocais: {
    title: 'Locais',
    subtitle: 'Locais disponíveis para os seus treinos.',
    icon: 'stadium',
    singular: 'local',
    endpoint: '/treinadores/me/locais',
    columns: [cols.nome, cols.descricao],
    fields: localFields,
  },
  treinadorTreinos: {
    title: 'Treinos',
    subtitle: 'Marque e acompanhe os seus treinos.',
    icon: 'event',
    singular: 'treino',
    endpoint: '/treinos',
    columns: treinoColumns,
    fields: treinoFields('/esportes', '/treinadores/me/locais'),
    // o treino precisa pertencer ao treinador logado
    defaults: (user) => ({ treinador_id: user.profile_id }),
    create: true,
    edit: true,
    remove: true,
  },

  // ---------- coordenador ----------
  coordenadorEsportes: {
    title: 'Esportes da instituição',
    subtitle: 'Esportes cadastrados pelos treinadores.',
    icon: 'sports_soccer',
    singular: 'esporte',
    endpoint: '/esportes/coordenador/me',
    columns: [cols.nome, cols.descricao],
    fields: esporteFields,
  },
  coordenadorLocais: {
    title: 'Locais',
    subtitle: 'Cadastre locais e vincule esportes e instituição.',
    icon: 'stadium',
    singular: 'local',
    endpoint: '/locais',
    columns: [cols.nome, cols.descricao],
    fields: localFields,
    create: true,
    edit: true,
    remove: true,
    actions: [{ id: 'links', icon: 'link', label: 'Vínculos' }],
    linksSportsEndpoint: '/esportes/coordenador/me',
  },

  // ---------- administrador ----------
  adminInstituicoes: {
    title: 'Instituições',
    subtitle: 'Todas as instituições cadastradas.',
    icon: 'account_balance',
    singular: 'instituição',
    endpoint: '/instituicoes',
    columns: [cols.nome, cols.descricao, { key: 'latitude', label: 'Lat.' }, { key: 'longitude', label: 'Long.' }],
    fields: [
      nome,
      descricao,
      { key: 'latitude', label: 'Latitude', type: 'number', step: 'any' },
      { key: 'longitude', label: 'Longitude', type: 'number', step: 'any' },
    ],
    create: true,
    edit: true,
    remove: true,
  },
  adminCoordenadores: {
    title: 'Coordenadores',
    subtitle: 'Perfis de coordenadores. O cadastro é feito pela tela de criar conta.',
    icon: 'badge',
    singular: 'coordenador',
    endpoint: '/coordenadores',
    columns: [cols.nome, cols.email, cols.bio],
    fields: [nome, email, bio],
    edit: true,
    remove: true,
  },
  adminTreinadores: {
    title: 'Treinadores',
    subtitle: 'Perfis de treinadores. O cadastro é feito pela tela de criar conta.',
    icon: 'sports',
    singular: 'treinador',
    endpoint: '/treinadores',
    columns: [cols.nome, cols.email, cols.bio],
    fields: [nome, email, bio],
    edit: true,
    remove: true,
  },
  adminAtletas: {
    title: 'Atletas',
    subtitle: 'Perfis de atletas. O cadastro é feito pela tela de criar conta.',
    icon: 'directions_run',
    singular: 'atleta',
    endpoint: '/atletas',
    columns: [cols.nome, cols.email, { key: 'ano', label: 'Ano' }, cols.bio],
    fields: [nome, email, { key: 'ano', label: 'Ano', type: 'number', required: true }, bio],
    edit: true,
    remove: true,
  },
  adminEsportes: {
    title: 'Esportes',
    subtitle: 'Todos os esportes do sistema.',
    icon: 'sports_soccer',
    singular: 'esporte',
    endpoint: '/esportes',
    columns: [cols.nome, cols.descricao],
    fields: esporteFields,
    create: true,
    edit: true,
    remove: true,
  },
  adminLocais: {
    title: 'Locais',
    subtitle: 'Todos os locais e seus vínculos.',
    icon: 'stadium',
    singular: 'local',
    endpoint: '/locais',
    columns: [cols.nome, cols.descricao],
    fields: localFields,
    create: true,
    edit: true,
    remove: true,
    actions: [{ id: 'links', icon: 'link', label: 'Vínculos' }],
    linksSportsEndpoint: '/esportes',
  },
  adminTreinos: {
    title: 'Treinos',
    subtitle: 'Todos os treinos agendados.',
    icon: 'event',
    singular: 'treino',
    endpoint: '/treinos',
    columns: treinoColumns,
    fields: [
      ...treinoFields('/esportes', '/locais'),
      { key: 'treinador_id', label: 'Treinador', type: 'select', required: true, only: 'create', optionsFrom: { endpoint: '/treinadores', value: 'id', label: 'nome' } },
    ],
    create: true,
    edit: true,
    remove: true,
  },
};

// Recursos de um único registro (perfil, instituição do coordenador)
export const singles = {
  perfil: (user) => {
    const byRole = {
      atleta: {
        endpoint: `/atletas/${user.profile_id}`,
        fields: [nome, email, { key: 'ano', label: 'Ano', type: 'number', required: true }, bio],
      },
      treinador: {
        endpoint: `/treinadores/${user.profile_id}`,
        fields: [nome, email, bio],
      },
      coordenador: {
        endpoint: `/coordenadores/${user.profile_id}`,
        fields: [nome, email, bio],
      },
    };
    return { title: 'Meu perfil', subtitle: 'Seus dados no Esportando.', icon: 'person', ...byRole[user.role] };
  },
  coordenadorInstituicao: (user) => ({
    title: 'Minha instituição',
    subtitle: 'Dados da instituição que você coordena.',
    icon: 'account_balance',
    endpoint: `/instituicoes/${user.institution_id}`,
    fields: [
      nome,
      descricao,
      { key: 'latitude', label: 'Latitude', type: 'number', step: 'any' },
      { key: 'longitude', label: 'Longitude', type: 'number', step: 'any' },
    ],
  }),
};
