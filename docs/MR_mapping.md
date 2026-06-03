# Mapeamento Relacional (MR) — Projeto Vendas

Este documento apresenta o mapeamento do Modelo Entidade-Relacionamento (MER) para o Modelo Relacional (MR), descreve tabelas, colunas, chaves, restrições e uma justificativa de normalização até a 3ª Forma Normal (3NF).

> Observação: o banco do projeto é SQLite e algumas colunas históricas receberam sufixos por migrações anteriores (ex.: `cliente_id_id`). Abaixo apresento o MR lógico (conceitual) e notas sobre discrepâncias físicas atuais.

---

## Entidades / Tabelas (MR)

1) `usuario` (model `Usuario` / tabela `Vendas_usuario`)
- PK: `id` (BIGINT / AutoField)
- Colunas:
  - `id` PK
  - `username` VARCHAR(150) UNIQUE
  - `password` VARCHAR(128)
  - `first_name`, `last_name` VARCHAR(150)
  - `is_staff`, `is_active`, `is_superuser` BOOLEAN
  - `date_joined` DATETIME
  - `nome` VARCHAR(100)
  - `idade` INTEGER
  - `cpf` VARCHAR(14)  -- atualmente NÃO marcado como UNIQUE no modelo
  - `telefone` VARCHAR(20)
  - `endereco` TEXT
  - `cidade` VARCHAR(100)
  - `email` VARCHAR

- Restrições relevantes:
  - `username` tem restrição de unicidade pelo Django.
  - Recomenda-se aplicar `UNIQUE` em `cpf` se for requisito de negócio.

---

2) `categoria` (model `Categoria` / tabela `Vendas_categoria`)
- PK: `id` (BIGINT)
- Colunas: `id`, `nome` VARCHAR(100), `descricao` TEXT
- Observações: sem FKs

---

3) `mercadoria` (model `Mercadoria` / tabela `Vendas_mercadoria`)
- PK: `id`
- Colunas: `id`, `nome`, `descricao`, `categoria_id` (FK → `categoria.id`)
- FK: `categoria_id` REFERENCES `Vendas_categoria(id)` ON DELETE CASCADE

---

4) `produto` (model `Produto` / tabela `Vendas_produto`)
- PK: `id`
- Colunas: `id`, `nome`, `preco` (DECIMAL), `mercadoria_id` (FK → `mercadoria.id`)
- FK: `mercadoria_id` REFERENCES `Vendas_mercadoria(id)` ON DELETE CASCADE

---

5) `estoque` (model `Estoque` / tabela `Vendas_estoque`)
- PK: `id`
- Colunas: `id`, `produto_id` (FK → `produto.id`), `quantidade` (INTEGER >= 0), `minimo_quantidade` (INTEGER >= 0)
- FK: `produto_id` REFERENCES `Vendas_produto(id)` ON DELETE CASCADE
- Observação: no MR lógico, a relação entre `produto` e `estoque` é conceitualmente 1:1 (um produto tem um registro de estoque). No modelo atual `Estoque` tem uma FK para `Produto`, o que modela adequadamente essa relação.

---

6) `venda` (model `Venda` / tabela `Vendas_venda`)
- PK: `id`
- Colunas: `id`, `data` DATETIME (auto_now_add), `usuario_id` (FK → `usuario.id`) — no DB atual pode aparecer como `cliente_id_id` devido a migrações históricas
- FK: `usuario_id` REFERENCES `Vendas_usuario(id)` ON DELETE CASCADE

---

7) `venda_produto` (model `Venda_Produto` / tabela `Vendas_venda_produto`)
- PK: `id`
- Colunas: `id`, `venda_id` (FK → `venda.id`), `produto_id` (FK → `produto.id`), `quantidade` INTEGER
- FKs: `venda_id` REFERENCES `Vendas_venda(id)`, `produto_id` REFERENCES `Vendas_produto(id)`
- Observação: esta tabela é a entidade associativa (associação N:N entre `venda` e `produto`) com atributo adicional `quantidade`.

---

## Mapeamento MER → MR (resumo)
- MER: `Venda` com vários `Produto` via relacionamento de itens → MR: tabela `venda` + tabela associativa `venda_produto`.
- MER: `Produto` pertence a uma `Mercadoria` que por sua vez pertence a uma `Categoria` → MR: FKs `produto.mercadoria_id` e `mercadoria.categoria_id`.
- MER: `Usuario` (Cliente) relacionado a `Venda` em 1:N → MR: `venda.usuario_id` FK para `usuario.id`.

---

## Restrições (PK, FK, integridade)
- PKs: todas as tabelas usam `id` (auto-increment) como PK.
- FKs: implementadas conforme declarado nos modelos; Django cria constraints e o comportamento `on_delete` (CASCADE) é aplicado conforme declarado.
- Restrições de unicidade: `username` é único; `cpf` atualmente NÃO é único, mas o README antigo citava `cpf` único para a entidade `Cliente` — se for regra de negócio, adicionar `unique=True` e migrar o DB.
- Not null: campos como `nome`/`preco` são NOT NULL pelo modelo (via ausência de `null=True`). Alguns campos do `Usuario` são opcionais (`blank=True, null=True`).

---

## Normalização — verificação até 3ª Forma Normal (3NF)

Objetivo: verificar que o MR satisfaça 1NF, 2NF e 3NF.

1NF (Primeira Forma Normal)
- Regras: atributos atômicos; cada campo contém apenas um valor atómico, sem grupos repetitivos.
- Situação: as tabelas usam colunas atômicas (ex.: `telefone` é um único campo textual — se for necessário armazenar múltiplos telefones por usuário, seria necessário criar tabela separada). Logo, 1NF é satisfeita.

2NF (Segunda Forma Normal)
- Regras: estar em 1NF e todos os atributos não-chave dependerem da chave primária inteira (aplica-se quando existe chave composta).
- Situação: as principais tabelas têm PK simples (`id`). A existência de `venda_produto` usa `id` como PK; alternativamente poderia usar chave composta `(venda_id, produto_id)`. Não há dependências parciais conhecidas. Portanto, 2NF é satisfeita.

3NF (Terceira Forma Normal)
- Regras: estar em 2NF e não ter dependências transitivas de atributos não-chave (ou seja, atributos não-chave não dependem de outros atributos não-chave).
- Situação: atributos como `produto.preco` dependem da entidade `produto` (chave da tabela) e não de outros atributos não-chave. Não existem atributos que sejam derivados de outros atributos não-chave dentro da mesma tabela. A separação `categoria`/`mercadoria`/`produto` evita repetição de `categoria.descricao` por produto. Assim, o modelo está em 3NF.

Observações adicionais sobre 3NF e potenciais melhorias:
- `Estoque` poderia ter a PK igual a `produto_id` (transformando-a em 1:1 com `produto`) em vez de `id` separado para reforçar a unicidade de estoque por produto.
- Se `cpf` realmente for único por pessoa, aplicar a restrição previne inconsistência e ajuda normalização de regras de negócio.

---

## Discrepâncias físicas observadas no DB atual
- Algumas colunas no arquivo `db.sqlite3` têm sufixos decorrentes de migrações antigas: `cliente_id_id`, `produto_id_id`, `venda_id_id`. Isto decorre de renomeações e mudanças na modelagem ao longo do desenvolvimento; o MR lógico desejado usa nomes `usuario_id`, `produto_id`, `venda_id` sem o sufixo duplicado.
- Recomendo criar uma migração manual com `RunSQL` para renomear colunas no banco (ou reconstruir a tabela) caso queira limpar o schema físico. Já adaptei os `db_column` nos modelos para compatibilidade com o estado físico atual; no longo prazo, alinhar nomes evita confusão.

---

## Atualizações Recentes (Junho/2026)

### Correções de Modelo
- `Venda` model: campo FK `usuario_id` (db_column: `cliente_id_id`) — as views foram corrigidas para usar `usuario_id` em vez de `usuario` nas queries (ex: `Venda.objects.filter(usuario_id=request.user)`)

### Restrições de Acesso (Admin)
- Dashboards e dados financeiros visíveis apenas para `user.is_staff`
- Operações CRUD protegidas no backend com `@admin_required`
- Templates condicionais: botões "Criar/Editar/Excluir" ocultos para usuários comuns

### Melhorias de Layout
- CSS refatorado com design moderno: fonte Inter, variáveis CSS, animações
- Logo do sistema: `Vendas/static/Vendas/images/image.png`
- Header e navbar sticky com tema escuro
- Design responsivo (mobile-first)

---

