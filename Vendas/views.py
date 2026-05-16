from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as login_django, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.paginator import Paginator 

# Create your views here.

# Listagem de categorias
def index(request):
    categorias = Categoria.objects.all()
    # paginação
    paginator = Paginator(categorias, 10)  # Exibe 10 categorias por página
    page = request.GET.get('page')
    categorias = paginator.get_page(page)

    context = {
        'categorias': categorias,
    }
    return render(request, 'index.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login_django(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciais inválidas. Tente novamente.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro bem-sucedido. Faça login para continuar.')
            return redirect('login')
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
    }

    return render(request, 'register.html', context)

# crud do cliente
def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso.')
            return redirect('index')
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
    }

    return render(request, 'cadastro_cliente.html', context)

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteEditForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            cliente.set_password(request.POST.get('password'))  # Atualiza a senha se fornecida
            return redirect('index')
    else:
        form = ClienteEditForm(instance=cliente)
    
    context = {
        'form': form,
    }

    return render(request, 'editar_cliente.html', context)

@login_required
def excluir_cliente(request, id):
    cliente=Cliente.objects.get(id=id)
    cliente.delete()
    return redirect('index')

#crud de categoria
def cadastro_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso.')
            return redirect('index')
    else:
        form = CategoriaForm()
    
    context = {
        'form': form,
    }

    return render(request, 'cadastro_categoria.html', context)

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {
        'form': form,
    }

    return render(request, 'editar_categoria.html', context)

@login_required
def excluir_categoria(request, id):
    categoria=Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('index')

#crud de mercadoria
def cadastro_mercadoria(request):
    if request.method == 'POST':
        form = MercadoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mercadoria cadastrada com sucesso.')
            return redirect('index')
    else:
        form = MercadoriaForm()
    
    context = {
        'form': form,
    }

    return render(request, 'cadastro_mercadoria.html', context)

@login_required
def editar_mercadoria(request, id):
    mercadoria = get_object_or_404(Mercadoria, id=id)
    if request.method == 'POST':
        form = MercadoriaForm(request.POST, instance=mercadoria)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = MercadoriaForm(instance=mercadoria)
    
    context = {
        'form': form,
    }

    return render(request, 'editar_mercadoria.html', context)

@login_required
def excluir_mercadoria(request, id):
    mercadoria=Mercadoria.objects.get(id=id)
    mercadoria.delete()
    return redirect('index')

#crud de produto
def cadastro_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso.')
            return redirect('index')
    else:
        form = ProdutoForm()
    
    context = {
        'form': form,
    }

    return render(request, 'cadastro_produto.html', context)

@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProdutoForm(instance=produto)
    
    context = {
        'form': form,
    }

    return render(request, 'editar_produto.html', context)

@login_required
def excluir_produto(request, id):
    produto=Produto.objects.get(id=id)
    produto.delete()
    return redirect('index')

#pagia de venda
def cadastro_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    cliente = Cliente.objects.get(id=venda.cliente_id)
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Venda cadastrada com sucesso.')
            return redirect('venda', venda_id=venda.id)
    else:
        form = VendaForm()
    
    context = {
        'clientes': cliente,
        'form': form,
    }

    return render(request, 'cadastro_venda.html', context)

#perfil 
@login_required
def perfil(request):
    cliente = request.user.cliente
    vendas = Venda.objects.filter(cliente_id=cliente.id).order_by('-data')
    
    # Aplicação do filtro
    vendas_filter = VendaFilterForm(request.GET, queryset=vendas)

    # Obtem o QuerySet filtrado diretamente e ordenado
    vendas_filtradas = vendas_filter.qs.order_by('-data')

    # Paginação
    paginator = Paginator(vendas_filtradas, 10)  # Exibe
    page = request.GET.get('page')
    vendas = paginator.get_page(page)

    context = {
        'cliente': cliente,
        'vendas': vendas,
        'vendas_filter': vendas_filter
    }
    return render(request, 'perfil.html', context)

#pagina de login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cliente = authenticate(request, username=username, password=password)
        
        if cliente:
            login_django(request, cliente)
            return redirect('index')

    return render(request, 'login.html')
