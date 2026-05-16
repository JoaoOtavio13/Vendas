# Vendas - Sistema de Gestão de Vendas

Um sistema de gestão de vendas desenvolvido em Django com funcionalidades de controle de estoque, produtos, categorias e vendas.

## Tecnologias

- **Python 3.x**
- **Django** - Framework web
- **SQLite** - Banco de dados
- **Django Admin** - Interface de administração

## Funcionalidades

✅ Gestão de Clientes
✅ Gestão de Categorias e Mercadorias
✅ Gestão de Produtos
✅ Controle de Estoque
✅ Registro de Vendas
✅ Validação de quantidade em estoque
✅ Interface administrativa via Django Admin

## Estrutura do Projeto

```
Vendas_ajustes/
├── main/                 # Configuração principal do Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── Vendas/               # App principal
│   ├── models.py        # Modelos de dados
│   ├── admin.py         # Configuração do admin
│   ├── views.py         # Views
│   ├── migrations/      # Migrações do banco
│   └── tests.py         # Testes
├── db.sqlite3           # Banco de dados
├── manage.py            # Script de gerenciamento
├── .gitignore           # Arquivo de ignorar versão
└── README.md            # Este arquivo
```

## Instalação e Setup

### 1. Clone o repositório
```bash
git clone https://github.com/JoaoOtavio13/Vendas.git
cd Vendas_ajustes
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install django
```

### 5. Execute as migrações
```bash
python manage.py migrate
```

### 6. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor
```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/admin/`

## Modelos de Dados

### Cliente
- Nome
- CPF (único)
- Email
- Idade
- Cidade

### Categoria
- Nome
- Descrição

### Mercadoria
- Nome
- Categoria (FK)
- Descrição

### Produto
- Nome
- Mercadoria (FK)
- Preço

### Estoque
- Produto (FK)
- Quantidade (PositiveIntegerField)
- Quantidade Mínima (PositiveIntegerField)

### Venda
- Cliente (FK)
- Data (auto_now_add)
- Método: `total()` - calcula total da venda

### Venda_Produto
- Venda (FK)
- Produto (FK)
- Quantidade
- Método: `subtotal()` - calcula subtotal do item
- Validação de estoque no `save()`

## Principais Features

### Validação de Estoque
Quando uma venda é registrada, o sistema:
- Valida se há quantidade suficiente em estoque
- Atualiza o estoque de forma transacional
- Impede vendas com estoque negativo

### Cálculo de Totais
- Cada item da venda calcula seu subtotal
- A venda calcula o total somando todos os itens

## Comandos Úteis

```bash
# Executar migrações
python manage.py migrate

# Criar novas migrações
python manage.py makemigrations

# Shell interativo do Django
python manage.py shell

# Ver status das migrações
python manage.py showmigrations

# Coletar arquivos estáticos (para produção)
python manage.py collectstatic
```

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto é de código aberto e disponível sob a licença MIT.

## Contato

**Autor:** João Otávio
**GitHub:** [JoaoOtavio13](https://github.com/JoaoOtavio13)
