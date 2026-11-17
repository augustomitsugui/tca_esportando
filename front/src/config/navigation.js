// Menus por perfil. "hint" aparece nos atalhos do painel.
export const navigation = {
  atleta: [
    { to: '/painel', label: 'Início', icon: 'home', exact: true },
    { to: '/atleta/esportes', label: 'Esportes', icon: 'sports_soccer', hint: 'Veja os esportes e peça para participar.' },
    { to: '/atleta/treinos', label: 'Treinos', icon: 'event', hint: 'Consulte sua agenda de treinos.' },
    { to: '/perfil', label: 'Meu perfil', icon: 'person', hint: 'Atualize seus dados.' },
  ],
  treinador: [
    { to: '/painel', label: 'Início', icon: 'home', exact: true },
    { to: '/treinador/esportes', label: 'Esportes', icon: 'sports_soccer', hint: 'Cadastre e organize seus esportes.' },
    { to: '/treinador/locais', label: 'Locais', icon: 'stadium', hint: 'Locais disponíveis para treinar.' },
    { to: '/treinador/treinos', label: 'Treinos', icon: 'event', hint: 'Marque e gerencie treinos.' },
    { to: '/treinador/solicitacoes', label: 'Pedidos', icon: 'mark_email_unread', hint: 'Atletas querendo entrar nos esportes.' },
    { to: '/treinador/atletas', label: 'Atletas', icon: 'groups', hint: 'Atletas vinculados aos seus esportes.' },
    { to: '/perfil', label: 'Meu perfil', icon: 'person', hint: 'Atualize seus dados.' },
  ],
  coordenador: [
    { to: '/painel', label: 'Início', icon: 'home', exact: true },
    { to: '/coordenador/instituicao', label: 'Instituição', icon: 'account_balance', hint: 'Dados da sua instituição.' },
    { to: '/coordenador/locais', label: 'Locais', icon: 'stadium', hint: 'Cadastre locais e vincule esportes.' },
    { to: '/coordenador/esportes', label: 'Esportes', icon: 'sports_soccer', hint: 'Esportes da instituição.' },
    { to: '/coordenador/solicitacoes', label: 'Pedidos', icon: 'how_to_reg', hint: 'Aprove ou recuse treinadores.' },
    { to: '/perfil', label: 'Meu perfil', icon: 'person', hint: 'Atualize seus dados.' },
  ],
  admin: [
    { to: '/admin', label: 'Visão geral', icon: 'dashboard', exact: true },
    { to: '/admin/solicitacoes', label: 'Solicitações', icon: 'how_to_reg', hint: 'Aprovações pendentes.' },
    { to: '/admin/instituicoes', label: 'Instituições', icon: 'account_balance', hint: 'Todas as instituições.' },
    { to: '/admin/coordenadores', label: 'Coordenadores', icon: 'badge', hint: 'Perfis de coordenadores.' },
    { to: '/admin/treinadores', label: 'Treinadores', icon: 'sports', hint: 'Perfis de treinadores.' },
    { to: '/admin/atletas', label: 'Atletas', icon: 'directions_run', hint: 'Perfis de atletas.' },
    { to: '/admin/esportes', label: 'Esportes', icon: 'sports_soccer', hint: 'Todos os esportes.' },
    { to: '/admin/locais', label: 'Locais', icon: 'stadium', hint: 'Todos os locais e vínculos.' },
    { to: '/admin/treinos', label: 'Treinos', icon: 'event', hint: 'Todos os treinos.' },
  ],
};
