from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as login_django, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
import json
from django.db import transaction
# Create your views here.

# Decorator para verificar se o usuário é admin
def admin_required(view_func):
    return user_passes_test(lambda user: user.is_staff, login_url='login')(view_func)

#Listagem de categorias
def index(request):
    categorias = Categoria.objects.all().annotate(total_mercadorias=Count('mercadoria'))
    paginator = Paginator(categorias, 3)
    page_number = request.GET.get('page')
    categorias = paginator.get_page(page_number)
    resumo_financeiro = ResumoFinanceiro.get_solo()
    context={
        'categorias': categorias,
        'resumo_financeiro': resumo_financeiro,
        'total_produtos': Produto.objects.count(),
        'total_mercadorias': Mercadoria.objects.count(),
    }
    return render(request, 'html/index.html', context)

#Listagem de mercadorias
def mercadorias(request, categoria_id=None):
    if categoria_id:
        categoria = get_object_or_404(Categoria, id=categoria_id)
        mercadorias = Mercadoria.objects.filter(categoria_id=categoria)
    else:
        categoria = None
        mercadorias = Mercadoria.objects.all()
    paginator = Paginator(mercadorias, 3)
    page_number = request.GET.get('page')
    mercadorias = paginator.get_page(page_number)
    context={
        'mercadorias': mercadorias,
        'categoria': categoria,
    }
    return render(request, 'html/mercadorias.html', context)


#Listagem de produtos por mercadoria
def produtos_por_mercadoria(request, mercadoria_id):
    mercadoria = get_object_or_404(Mercadoria, id=mercadoria_id)
    produtos = Produto.objects.filter(mercadoria_id=mercadoria)
    paginator = Paginator(produtos, 3)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)
    context = {
        'produtos': produtos,
        'mercadoria': mercadoria,
    }
    return render(request, 'html/produtos.html', context)


#Listagem de produtos
def produtos(request):
    produtos = Produto.objects.all()
    paginator = Paginator(produtos, 3)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)
    context={
        'produtos': produtos
    }
    return render(request, 'html/produtos.html', context)


class ProdutoListView(ListView):
    model = Produto
    template_name = 'html/produtos.html'
    context_object_name = 'produtos'
    paginate_by = 3


class VendaDetailView(DetailView):
    model = Venda
    template_name = 'html/venda.html'
    context_object_name = 'venda'


@login_required
@admin_required
def criar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.save()
            messages.success(request, f'Venda #{venda.id} criada com sucesso! Agora adicione os itens.')
            return redirect('editar_venda', pk=venda.pk)
    else:
        form = VendaForm()

    return render(request, 'html/criar_venda.html', {'form': form})


@login_required
@admin_required
def editar_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)

    if request.method == 'POST':
        form = VendaProdutoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            if item.venda_id_id != venda.id:
                item.venda_id = venda
            try:
                item.save()
                messages.success(request, 'Item adicionado à venda com sucesso!')
                return redirect('venda_detail', pk=venda.pk)
            except ValidationError as e:
                # Se a venda não tem nenhum item, remove a venda do banco
                if venda.itens.count() == 0:
                    venda.delete()
                    messages.error(request, 'Venda cancelada — ' + (e.messages[0] if hasattr(e, 'messages') else str(e)))
                    return redirect('criar_venda')
                messages.error(request, e.messages[0] if hasattr(e, 'messages') else str(e))
    else:
        form = VendaProdutoForm(initial={'venda_id': venda})

    return render(request, 'html/editar_venda.html', {'form': form, 'venda': venda})

#crud de usuarios
def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
    else:
        form = UsuarioForm()
    context = {
        'form': form
    }
    return render(request, 'html/cadastro.html', context)


@csrf_exempt
def api_register(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'detail': 'Invalid JSON'}, status=400)

    username = payload.get('username')
    password1 = payload.get('password1')
    password2 = payload.get('password2')
    email = payload.get('email')

    if not username or not password1 or not password2:
        return JsonResponse({'detail': 'username and passwords are required'}, status=400)
    if password1 != password2:
        return JsonResponse({'detail': 'passwords do not match'}, status=400)

    # create user
    try:
        user = Usuario.objects.create_user(username=username, email=email, password=password1)
        # optional fields
        user.nome = payload.get('nome') or ''
        user.idade = payload.get('idade') or None
        user.cpf = payload.get('cpf') or ''
        user.telefone = payload.get('telefone') or ''
        user.endereco = payload.get('endereco') or ''
        user.cidade = payload.get('cidade') or ''
        # email already set above
        user.save()
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=400)

    return JsonResponse({'id': user.id, 'username': user.username}, status=201)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_django(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            if user.is_staff:
                return redirect('index')
            return redirect('perfil')
        else:
            messages.error(request, 'Credenciais inválidas. Tente novamente.')
    return render(request, 'html/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('index')

@login_required
def editar_usuario(request,id):
    usuario = Usuario.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil editado com sucesso!')
            return redirect('perfil')
    else:
        form = UsuarioEditForm(instance=usuario)
    context = {
        'form': form
    }
    return render(request, 'html/editar_usuario.html', context)

@login_required
def excluir_usuario(request, id):
    usuario=Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('index')

#crud de categorias apenas para admin
@login_required
def categorias(request):
    categorias = Categoria.objects.all().annotate(total_mercadorias=Count('mercadoria'))
    paginator = Paginator(categorias, 3)
    page_number = request.GET.get('page')
    categorias = paginator.get_page(page_number)
    context={
        'categorias': categorias
    }
    return render(request, 'html/categorias.html', context)

@login_required
@admin_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('index')
    else:
        form = CategoriaForm()
    context = {
        'form': form
    }
    return render(request, 'html/criar_categoria.html', context) 

@login_required
@admin_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria editada com sucesso!')
            return redirect('index')
    else:
        form = CategoriaForm(instance=categoria)
    context = {
        'form': form,
        'categoria': categoria
    }
    return render(request, 'html/editar_categoria.html', context)

@login_required
@admin_required
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('index')
    context = {
        'categoria': categoria
    }
    return render(request, 'html/excluir_categoria.html', context)

def filtrar_categorias(request):
    form = CategoriaFilterForm(request.GET)
    categorias = form.qs
    context = {
        'form': form,
        'categorias': categorias
    }
    return render(request, 'html/filtrar_categorias.html', context)

#crud de mercadorias apenas para admin
@login_required
@admin_required
def criar_mercadoria(request):
    if request.method == 'POST':
        form = MercadoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mercadoria criada com sucesso!')
            return redirect('mercadorias')
    else:
        form = MercadoriaForm()
    context = {
        'form': form
    }
    return render(request, 'html/criar_mercadoria.html', context)

@login_required
@admin_required
def editar_mercadoria(request, mercadoria_id):
    mercadoria = get_object_or_404(Mercadoria, id=mercadoria_id)
    if request.method == 'POST':
        form = MercadoriaForm(request.POST, request.FILES, instance=mercadoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mercadoria editada com sucesso!')
            return redirect('mercadorias')
    else:
        form = MercadoriaForm(instance=mercadoria)
    context = {
        'form': form,
        'mercadoria': mercadoria
    }
    return render(request, 'html/editar_mercadoria.html', context)

@login_required
@admin_required
def excluir_mercadoria(request, mercadoria_id):
    mercadoria = get_object_or_404(Mercadoria, id=mercadoria_id)
    if request.method == 'POST':
        mercadoria.delete()
        messages.success(request, 'Mercadoria excluída com sucesso!')
        return redirect('mercadorias')
    context = {
        'mercadoria': mercadoria
    }
    return render(request, 'html/excluir_mercadoria.html', context)

def filtrar_mercadorias(request):
    form = MercadoriaFilterForm(request.GET)
    mercadorias = form.qs
    context = {
        'form': form,
        'mercadorias': mercadorias
    }
    return render(request, 'html/filtrar_mercadorias.html', context)

#crud de produtos apenas para admin
@login_required
@admin_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('produtos')
    else:
        form = ProdutoForm()
    context = {
        'form': form
    }
    return render(request, 'html/criar_produto.html', context)

@login_required
@admin_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProdutoEditForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto editado com sucesso!')
            return redirect('produtos')
    else:
        form = ProdutoEditForm(instance=produto)
    context = {
        'form': form,
        'produto': produto
    }
    return render(request, 'html/editar_produto.html', context)

@login_required
@admin_required
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('produtos')
    context = {
        'produto': produto
    }
    return render(request, 'html/excluir_produto.html', context)

def filtrar_produtos(request):
    form = ProdutoFilterForm(request.GET)
    produtos = form.qs
    context = {
        'form': form,
        'produtos': produtos
    }
    return render(request, 'html/filtrar_produtos.html', context)

#CRUD de Estoque (admin)
@login_required
@admin_required
def lista_estoque(request):
    estoques = Estoque.objects.select_related('produto_id__mercadoria_id').all()
    paginator = Paginator(estoques, 10)
    page_number = request.GET.get('page')
    estoques = paginator.get_page(page_number)
    return render(request, 'html/lista_estoque.html', {'estoques': estoques})


@login_required
@admin_required
def criar_estoque(request):
    if request.method == 'POST':
        form = EstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estoque criado com sucesso!')
            return redirect('lista_estoque')
    else:
        form = EstoqueForm()
    return render(request, 'html/criar_estoque.html', {'form': form})


@login_required
@admin_required
def editar_estoque(request, estoque_id):
    estoque = get_object_or_404(Estoque, id=estoque_id)
    if request.method == 'POST':
        form = EstoqueEditForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            messages.success(request, f'Estoque de "{estoque.produto_id.nome}" atualizado com sucesso!')
            return redirect('lista_estoque')
    else:
        form = EstoqueEditForm(instance=estoque)
    return render(request, 'html/editar_estoque.html', {'form': form, 'estoque': estoque})

#Listagem de todas as vendas (admin)
@login_required
@admin_required
def lista_vendas(request):
    from datetime import datetime, date
    
    vendas = Venda.objects.all().order_by('-data')
    
    # Filtro por data (GET parameters: data_inicio e data_fim)
    data_inicio = request.GET.get('data_inicio', '').strip()
    data_fim = request.GET.get('data_fim', '').strip()
    
    try:
        if data_inicio:
            data_inicio_parsed = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            vendas = vendas.filter(data__gte=data_inicio_parsed)
    except (ValueError, TypeError):
        data_inicio = ''
    
    try:
        if data_fim:
            data_fim_parsed = datetime.strptime(data_fim, '%Y-%m-%d').date()
            from datetime import timedelta
            # data_fim deve incluir todo o dia, então vamos até o final do dia
            data_fim_end = datetime.combine(data_fim_parsed, datetime.max.time())
            vendas = vendas.filter(data__lte=data_fim_end)
    except (ValueError, TypeError):
        data_fim = ''
    
    paginator = Paginator(vendas, 10)
    page_number = request.GET.get('page')
    vendas_page = paginator.get_page(page_number)
    
    context = {
        'vendas': vendas_page,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'html/lista_vendas.html', context)


# ========== CARRINHO DE COMPRAS ==========

@login_required
def adicionar_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    # Busca um carrinho aberto para o usuário, ou cria um novo
    carrinho, created = Venda.objects.get_or_create(
        usuario_id=request.user,
        status='carrinho',
        defaults={'usuario_id': request.user}
    )
    
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))
        if quantidade < 1:
            messages.error(request, 'Quantidade inválida.')
            return redirect('produtos')
        
        # Verifica se o produto já está no carrinho
        item_existente = Venda_Produto.objects.filter(
            venda_id=carrinho,
            produto_id=produto
        ).first()
        
        if item_existente:
            # Se já existe, aumenta a quantidade
            item_existente.quantidade += quantidade
            try:
                item_existente.save()
                messages.success(request, f'Quantidade de "{produto.nome}" atualizada no carrinho!')
            except ValidationError as e:
                messages.error(request, e.messages[0] if hasattr(e, 'messages') else str(e))
                return redirect('ver_carrinho')
        else:
            # Cria novo item
            item = Venda_Produto(
                venda_id=carrinho,
                produto_id=produto,
                quantidade=quantidade
            )
            try:
                item.save()
                messages.success(request, f'"{produto.nome}" adicionado ao carrinho!')
            except ValidationError as e:
                messages.error(request, e.messages[0] if hasattr(e, 'messages') else str(e))
                return redirect('produtos')
        
        return redirect('ver_carrinho')
    
    # GET: mostra página de confirmação do produto
    return render(request, 'html/adicionar_carrinho.html', {
        'produto': produto,
        'carrinho': carrinho,
    })


@login_required
def ver_carrinho(request):
    carrinho = Venda.objects.filter(
        usuario_id=request.user,
        status='carrinho'
    ).first()
    
    context = {
        'carrinho': carrinho,
    }
    return render(request, 'html/carrinho.html', context)


@login_required
def editar_item_carrinho(request, item_id):
    item = get_object_or_404(Venda_Produto, id=item_id, venda_id__usuario_id=request.user)
    
    if request.method == 'POST':
        nova_quantidade = int(request.POST.get('quantidade', 1))
        if nova_quantidade < 1:
            messages.error(request, 'A quantidade mínima é 1.')
            return redirect('ver_carrinho')
        
        item.quantidade = nova_quantidade
        try:
            item.save()
            messages.success(request, f'Quantidade de "{item.produto_id.nome}" atualizada!')
        except ValidationError as e:
            messages.error(request, e.messages[0] if hasattr(e, 'messages') else str(e))
        
        return redirect('ver_carrinho')
    
    return redirect('ver_carrinho')


@login_required
def remover_item_carrinho(request, item_id):
    item = get_object_or_404(Venda_Produto, id=item_id, venda_id__usuario_id=request.user)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'"{item.produto_id.nome}" removido do carrinho!')
        return redirect('ver_carrinho')
    
    return render(request, 'html/remover_item.html', {'item': item})


@login_required
def finalizar_compra(request):
    carrinho = get_object_or_404(Venda, usuario_id=request.user, status='carrinho')
    
    if carrinho.itens.count() == 0:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('ver_carrinho')
    
    if request.method == 'POST':
        carrinho.status = 'finalizada'
        carrinho.save()
        messages.success(request, f'Compra #{carrinho.id} finalizada com sucesso!')
        return redirect('perfil')
    
    return render(request, 'html/finalizar_compra.html', {'carrinho': carrinho})


#perfil do usuário
@login_required
def perfil(request):
    usuario = Usuario.objects.get(id=request.user.id)
    compras = Venda.objects.filter(usuario_id=request.user, status='finalizada').order_by('-data')
    compras_filter = VendaFilterForm(request.GET, queryset=compras)
    paginator = Paginator(compras, 5)
    page = request.GET.get('page')
    compras = paginator.get_page(page)

    context = {
        'usuario': usuario,
        'compras_filter': compras_filter,
        'compras': compras
    }
    return render(request, 'html/perfil.html', context)

