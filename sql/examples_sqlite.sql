-- Exemplos SQL para o projeto Vendas (SQLite)
-- Execute estes comandos no sqlite3 ou em um cliente compatível com SQLite.

PRAGMA foreign_keys = ON;

-- === Esquema (nomes canônicos/lógicos) ===
-- Observação: se seu arquivo SQLite atual usa nomes físicos diferentes (ex.: cliente_id_id), adapte os nomes abaixo conforme necessário.

CREATE TABLE IF NOT EXISTS Vendas_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    nome TEXT,
    idade INTEGER,
    cpf TEXT,
    telefone TEXT,
    endereco TEXT,
    cidade TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS Vendas_categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS Vendas_mercadoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    descricao TEXT,
    FOREIGN KEY(categoria_id) REFERENCES Vendas_categoria(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Vendas_produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    mercadoria_id INTEGER NOT NULL,
    preco REAL NOT NULL,
    FOREIGN KEY(mercadoria_id) REFERENCES Vendas_mercadoria(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Vendas_estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL UNIQUE,
    quantidade INTEGER DEFAULT 0,
    minimo_quantidade INTEGER DEFAULT 0,
    FOREIGN KEY(produto_id) REFERENCES Vendas_produto(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Vendas_venda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    data DATETIME DEFAULT (datetime('now')),
    FOREIGN KEY(usuario_id) REFERENCES Vendas_usuario(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Vendas_venda_produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY(venda_id) REFERENCES Vendas_venda(id) ON DELETE CASCADE,
    FOREIGN KEY(produto_id) REFERENCES Vendas_produto(id) ON DELETE CASCADE
);

-- === Inserção de dados de exemplo ===
BEGIN TRANSACTION;

INSERT INTO Vendas_usuario (username, password, nome, idade, cpf, telefone, endereco, cidade, email)
VALUES
('joao.otavio', 'pbkdf2_sha256$exemplo', 'João Otávio', 28, '12345678900', '(11)99999-9999', 'Rua A, 123', 'São Paulo', 'joao@example.com'),
('maria.silva', 'pbkdf2_sha256$exemplo', 'Maria Silva', 35, '98765432100', '(11)98888-8888', 'Rua B, 45', 'Rio de Janeiro', 'maria@example.com');

INSERT INTO Vendas_categoria (nome, descricao) VALUES
('Eletrônicos', 'Eletrônicos em geral'),
('Alimentos', 'Produtos alimentícios');

INSERT INTO Vendas_mercadoria (nome, categoria_id, descricao) VALUES
('Smartphones', 1, 'Telefones inteligentes'),
('Snacks', 2, 'Lanches e salgadinhos');

INSERT INTO Vendas_produto (nome, mercadoria_id, preco) VALUES
('Phone Model A', 1, 1299.90),
('Phone Model B', 1, 899.50),
('Snack Pack', 2, 5.50);

INSERT INTO Vendas_estoque (produto_id, quantidade, minimo_quantidade) VALUES
(1, 10, 2),
(2, 5, 1),
(3, 100, 10);

-- Criar uma venda e itens da venda
INSERT INTO Vendas_venda (usuario_id) VALUES (1);
INSERT INTO Vendas_venda_produto (venda_id, produto_id, quantidade) VALUES
(1, 1, 1),
(1, 3, 4);

COMMIT;

-- === Consultas básicas ===
-- 1) Listar todos os produtos com sua categoria e quantidade em estoque
SELECT p.id, p.nome AS produto, p.preco, m.nome AS mercadoria, c.nome AS categoria, e.quantidade
FROM Vendas_produto p
JOIN Vendas_mercadoria m ON p.mercadoria_id = m.id
JOIN Vendas_categoria c ON m.categoria_id = c.id
LEFT JOIN Vendas_estoque e ON e.produto_id = p.id;

-- 2) Mostrar vendas com itens (junção venda -> venda_produto -> produto)
SELECT v.id AS venda_id, v.data, u.username AS cliente, vp.produto_id, p.nome AS produto, vp.quantidade, p.preco, (vp.quantidade * p.preco) AS subtotal
FROM Vendas_venda v
JOIN Vendas_usuario u ON v.usuario_id = u.id
JOIN Vendas_venda_produto vp ON vp.venda_id = v.id
JOIN Vendas_produto p ON p.id = vp.produto_id
ORDER BY v.id, vp.id;

-- 3) Valor total por venda
SELECT v.id AS venda_id, u.username AS cliente, SUM(vp.quantidade * p.preco) AS total_venda
FROM Vendas_venda v
JOIN Vendas_usuario u ON v.usuario_id = u.id
JOIN Vendas_venda_produto vp ON vp.venda_id = v.id
JOIN Vendas_produto p ON p.id = vp.produto_id
GROUP BY v.id, u.username;

-- === Agregações / GROUP BY / HAVING ===
-- 4) Quantidade total vendida por produto
SELECT p.id, p.nome, SUM(vp.quantidade) AS total_vendido, SUM(vp.quantidade * p.preco) AS valor_total
FROM Vendas_venda_produto vp
JOIN Vendas_produto p ON p.id = vp.produto_id
GROUP BY p.id, p.nome
ORDER BY total_vendido DESC;

-- 5) Produtos com total vendido > 10 unidades
SELECT p.id, p.nome, SUM(vp.quantidade) AS total_vendido
FROM Vendas_venda_produto vp
JOIN Vendas_produto p ON p.id = vp.produto_id
GROUP BY p.id, p.nome
HAVING SUM(vp.quantidade) > 10;

-- === Exemplos de UPDATE / DELETE ===
-- 6) Atualizar estoque após correção manual
UPDATE Vendas_estoque SET quantidade = quantidade + 10 WHERE produto_id = 2;

-- 7) Remover um produto (cascata removerá estoque e referências em venda_produto via FK ON DELETE CASCADE)
DELETE FROM Vendas_produto WHERE id = 99; -- exemplo de id

-- === Exemplo transacional de inserção de venda (seguro) ===
-- Cria a venda, insere itens e decrementa o estoque em uma transação
BEGIN TRANSACTION;
INSERT INTO Vendas_venda (usuario_id) VALUES (2);
-- last_insert_rowid() retorna o id da última linha inserida no SQLite
INSERT INTO Vendas_venda_produto (venda_id, produto_id, quantidade) VALUES (last_insert_rowid(), 2, 1);
UPDATE Vendas_estoque SET quantidade = quantidade - 1 WHERE produto_id = 2 AND quantidade >= 1;
COMMIT;

-- === Consultas de diagnóstico úteis ===
-- 8) Listar produtos com estoque baixo (abaixo ou igual ao mínimo)
SELECT p.id, p.nome, e.quantidade, e.minimo_quantidade
FROM Vendas_estoque e
JOIN Vendas_produto p ON p.id = e.produto_id
WHERE e.quantidade <= e.minimo_quantidade;

-- Fim dos exemplos
