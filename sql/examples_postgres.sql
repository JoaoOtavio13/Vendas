-- Exemplos SQL para o projeto Vendas (PostgreSQL)
-- Execute em psql ou outro cliente PostgreSQL

-- Observação: adapte nomes de esquema/tabela conforme necessário.

SET client_min_messages = WARNING;

-- === Criação das tabelas (Modelo Relacional) ===

CREATE TABLE IF NOT EXISTS vendas_usuario (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nome VARCHAR(100),
    idade INTEGER,
    cpf VARCHAR(14), -- definir UNIQUE se for regra de negócio
    telefone VARCHAR(20),
    endereco TEXT,
    cidade VARCHAR(100),
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS vendas_categoria (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS vendas_mercadoria (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria_id BIGINT NOT NULL REFERENCES vendas_categoria(id) ON DELETE CASCADE,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS vendas_produto (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    mercadoria_id BIGINT NOT NULL REFERENCES vendas_mercadoria(id) ON DELETE CASCADE,
    preco NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS vendas_estoque (
    id BIGSERIAL PRIMARY KEY,
    produto_id BIGINT NOT NULL UNIQUE REFERENCES vendas_produto(id) ON DELETE CASCADE,
    quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
    minimo_quantidade INTEGER NOT NULL DEFAULT 0 CHECK (minimo_quantidade >= 0)
);

CREATE TABLE IF NOT EXISTS vendas_venda (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES vendas_usuario(id) ON DELETE CASCADE,
    data TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS vendas_venda_produto (
    id BIGSERIAL PRIMARY KEY,
    venda_id BIGINT NOT NULL REFERENCES vendas_venda(id) ON DELETE CASCADE,
    produto_id BIGINT NOT NULL REFERENCES vendas_produto(id) ON DELETE CASCADE,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0)
);

-- Índices úteis
CREATE INDEX IF NOT EXISTS idx_produto_mercadoria ON vendas_produto (mercadoria_id);
CREATE INDEX IF NOT EXISTS idx_venda_usuario ON vendas_venda (usuario_id);
CREATE INDEX IF NOT EXISTS idx_vendaprod_venda ON vendas_venda_produto (venda_id);
CREATE INDEX IF NOT EXISTS idx_vendaprod_produto ON vendas_venda_produto (produto_id);

-- === Exemplos de INSERTs (dados de teste) ===
BEGIN;

INSERT INTO vendas_usuario (username, password, nome, idade, cpf, telefone, endereco, cidade, email)
VALUES
('joao.otavio', 'hashed_pw_exemplo', 'João Otávio', 28, '12345678900', '(11)99999-9999', 'Rua Exemplo, 123', 'São Paulo', 'joao@example.com'),
('maria.silva', 'hashed_pw_exemplo', 'Maria Silva', 35, '98765432100', '(11)98888-8888', 'Rua B, 45', 'Rio de Janeiro', 'maria@example.com');

INSERT INTO vendas_categoria (nome, descricao) VALUES
('Eletrônicos', 'Produtos eletrônicos'),
('Alimentos', 'Produtos alimentícios');

INSERT INTO vendas_mercadoria (nome, categoria_id, descricao) VALUES
('Smartphones', 1, 'Telefones inteligentes'),
('Snacks', 2, 'Lanches e salgadinhos');

INSERT INTO vendas_produto (nome, mercadoria_id, preco) VALUES
('Phone Model A', 1, 1299.90),
('Phone Model B', 1, 899.50),
('Snack Pack', 2, 5.50);

INSERT INTO vendas_estoque (produto_id, quantidade, minimo_quantidade) VALUES
(1, 10, 2),
(2, 5, 1),
(3, 100, 10);

-- criar uma venda
INSERT INTO vendas_venda (usuario_id) VALUES (1) RETURNING id;
-- supondo que a venda retornou id = 1
INSERT INTO vendas_venda_produto (venda_id, produto_id, quantidade) VALUES
(1, 1, 1),
(1, 3, 4);

COMMIT;

-- === Consultas básicas e avançadas ===

-- 1) Listar produtos com sua mercadoria, categoria e quantidade em estoque
SELECT p.id, p.nome AS produto, p.preco, m.nome AS mercadoria, c.nome AS categoria, e.quantidade
FROM vendas_produto p
JOIN vendas_mercadoria m ON p.mercadoria_id = m.id
JOIN vendas_categoria c ON m.categoria_id = c.id
LEFT JOIN vendas_estoque e ON e.produto_id = p.id
ORDER BY p.id;

-- 2) Consultar vendas com itens e subtotais
SELECT v.id AS venda_id, v.data, u.username AS cliente, vp.produto_id, p.nome AS produto, vp.quantidade, p.preco, (vp.quantidade * p.preco) AS subtotal
FROM vendas_venda v
JOIN vendas_usuario u ON v.usuario_id = u.id
JOIN vendas_venda_produto vp ON vp.venda_id = v.id
JOIN vendas_produto p ON p.id = vp.produto_id
ORDER BY v.id, vp.id;

-- 3) Total por venda
SELECT v.id AS venda_id, u.username AS cliente, SUM(vp.quantidade * p.preco) AS total_venda
FROM vendas_venda v
JOIN vendas_usuario u ON v.usuario_id = u.id
JOIN vendas_venda_produto vp ON vp.venda_id = v.id
JOIN vendas_produto p ON p.id = vp.produto_id
GROUP BY v.id, u.username
ORDER BY total_venda DESC;

-- === Agrupamentos e HAVING ===

-- 4) Quantidade total vendida por produto
SELECT p.id, p.nome, SUM(vp.quantidade) AS total_vendido, SUM(vp.quantidade * p.preco) AS valor_total
FROM vendas_venda_produto vp
JOIN vendas_produto p ON p.id = vp.produto_id
GROUP BY p.id, p.nome
ORDER BY total_vendido DESC;

-- 5) Produtos com total vendido > 10 unidades
SELECT p.id, p.nome, SUM(vp.quantidade) AS total_vendido
FROM vendas_venda_produto vp
JOIN vendas_produto p ON p.id = vp.produto_id
GROUP BY p.id, p.nome
HAVING SUM(vp.quantidade) > 10;

-- === UPDATE / DELETE ===

-- 6) Atualizar estoque (ex.: receber 10 unidades para produto 2)
UPDATE vendas_estoque SET quantidade = quantidade + 10 WHERE produto_id = 2;

-- 7) Remover produto (cascata removerá estoques e referências em venda_produto)
DELETE FROM vendas_produto WHERE id = 99; -- exemplo

-- === Inserção de venda com transação segura (exemplo) ===
-- Exemplo em função anônima para demonstrar operação transacional
BEGIN;
INSERT INTO vendas_venda (usuario_id) VALUES (2) RETURNING id;
-- capture id retornado no cliente; em psql pode usar WITH ... ou executar em aplicação
-- Ex.: inserir item e ajustar estoque
INSERT INTO vendas_venda_produto (venda_id, produto_id, quantidade) VALUES (currval(pg_get_serial_sequence('vendas_venda','id')), 2, 1);
UPDATE vendas_estoque SET quantidade = quantidade - 1 WHERE produto_id = 2 AND quantidade >= 1;
COMMIT;

-- === Consultas de diagnóstico ===

-- 8) Produtos com estoque baixo (<= minimo)
SELECT p.id, p.nome, e.quantidade, e.minimo_quantidade
FROM vendas_estoque e
JOIN vendas_produto p ON p.id = e.produto_id
WHERE e.quantidade <= e.minimo_quantidade;

-- 9) Clientes mais ativos (por número de vendas)
SELECT u.id, u.username, COUNT(v.id) AS total_vendas
FROM vendas_usuario u
LEFT JOIN vendas_venda v ON v.usuario_id = u.id
GROUP BY u.id, u.username
ORDER BY total_vendas DESC;

-- Fim dos exemplos PostgreSQL
