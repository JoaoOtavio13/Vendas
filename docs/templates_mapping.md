# Mapeamento de Views → Templates

- index: Vendas/templates/html/index.html
- mercadorias: Vendas/templates/html/mercadorias.html
- produtos / `ProdutoListView`: Vendas/templates/html/produtos.html
- venda / `VendaDetailView`: Vendas/templates/html/venda.html
- cadastro_usuario: Vendas/templates/html/cadastro.html
- login: Vendas/templates/html/login.html
- editar_usuario: Vendas/templates/html/editar_usuario.html
- criar_categoria: Vendas/templates/html/criar_categoria.html
- editar_categoria: Vendas/templates/html/editar_categoria.html
- excluir_categoria: Vendas/templates/html/excluir_categoria.html
- filtrar_categorias: Vendas/templates/html/filtrar_categorias.html
- criar_mercadoria: Vendas/templates/html/criar_mercadoria.html
- editar_mercadoria: Vendas/templates/html/editar_mercadoria.html
- excluir_mercadoria: Vendas/templates/html/excluir_mercadoria.html
- filtrar_mercadorias: Vendas/templates/html/filtrar_mercadorias.html
- criar_produto: Vendas/templates/html/criar_produto.html
- editar_produto: Vendas/templates/html/editar_produto.html
- excluir_produto: Vendas/templates/html/excluir_produto.html
- filtrar_produtos: Vendas/templates/html/filtrar_produtos.html
- perfil: Vendas/templates/html/perfil.html

Observação: os templates estão em `Vendas/templates/html/`. As views foram atualizadas para usar esse caminho (render(request, 'html/<nome>.html')).
- editar_venda: Vendas/templates/html/editar_venda.html
- venda_detail / `VendaDetailView`: Vendas/templates/html/venda.html
- criar_venda: Vendas/templates/html/criar_venda.html

## Template Base (Vendas/templates/html/base.html)
- Logo: `<img src="{% static 'Vendas/images/image.png' %}" alt="Atacadão do João">` no `.brand-chip`
- Navegação (`.rolebar`) difere por perfil:
  - **Admin**: Categorias, Mercadorias, Cadastrar Produtos, Ver Produtos, Vendas, Perfil
  - **Usuário comum**: Início, Ver Produtos, Meu perfil
  - **Anônimo**: Login, Cadastro
- Dashboard (`.dashboard-strip`) visível apenas para admin (`{% if user.is_staff %}`)

## Restrições de Admin nos Templates
- `index.html`: dashboard (Mercadorias cadastradas, Produtos cadastrados, Faturamento total) visível apenas para `user.is_staff`
- `produtos.html`: botão "Criar produto" e links "Editar/Excluir" visíveis apenas para `user.is_staff`
- Views protegidas no backend com decorador `@admin_required`:
  - `criar_produto`, `editar_produto`, `excluir_produto`
  - `criar_categoria`, `editar_categoria`, `excluir_categoria`
  - `criar_mercadoria`, `editar_mercadoria`, `excluir_mercadoria`
  - `criar_venda`, `editar_venda`

## Estilo (Vendas/static/Vendas/css/style.css)
- Design moderno com variáveis CSS, fonte Inter (Google Fonts)
- Header escuro (`#1a1a2e`) com logo terracota (`#e07a5f`)
- Header e navbar sticky com efeitos hover
- Cards com sombras, bordas arredondadas e animações de fade-in
- Botões estilo pílula com transições suaves
- Layout responsivo (mobile-first, breakpoint 768px)
- Animações stagger (fadeInUp) nos cards de produtos

## Arquivos Estáticos
- Logo: `Vendas/static/Vendas/images/image.png`
- CSS: `Vendas/static/Vendas/css/style.css`

## Correções Recentes
- `perfil` view: corrigido `usuario=request.user` → `usuario_id=request.user` (FieldError)
