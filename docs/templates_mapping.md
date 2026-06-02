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
