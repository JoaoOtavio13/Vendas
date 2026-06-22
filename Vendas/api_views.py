from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404

from .models import Usuario, Categoria, Mercadoria, Produto, Estoque, ResumoFinanceiro, Venda, Venda_Produto
from .serializers import (
    UsuarioSerializer,
    CategoriaSerializer,
    MercadoriaSerializer,
    ProdutoSerializer,
    EstoqueSerializer,
    ProdutoComEstoqueSerializer,
    ResumoFinanceiroSerializer,
    VendaSerializer,
    VendaProdutoSerializer,
)


# ==================== AUTENTICAÇÃO ====================

class RegisterView(generics.CreateAPIView):
    """Endpoint para criar conta de usuário"""
    queryset = Usuario.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UsuarioSerializer


class LoginView(TokenObtainPairView):
    """Endpoint para login - retorna access_token e refresh_token JWT"""
    permission_classes = [AllowAny]


# ==================== PERMISSÃO PERSONALIZADA ====================

class IsDonoPermission(permissions.BasePermission):
    """
    Permissão personalizada: só permite acesso se o usuário for o dono da empresa.
    Consideramos 'dono' como o superusuário (is_superuser) ou um usuário específico.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


# ==================== PRODUTOS (ViewSet - CRUD completo) ====================

class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de produtos.
    - Listar todos os produtos / Criar produto
    - GET/POST/PUT/DELETE
    - Requer autenticação para criar/editar/deletar
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_permissions(self):
        """
        - Qualquer um pode listar (GET)
        - Só autenticados podem criar/editar/deletar
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [p() for p in permission_classes]


# ==================== DETALHES DO PRODUTO COM ESTOQUE ====================

class ProdutoDetailComEstoqueView(generics.RetrieveAPIView):
    """
    Endpoint para listar os detalhes de um produto específico junto com seu estoque.
    Requer autenticação.
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoComEstoqueSerializer
    permission_classes = [IsAuthenticated]


# ==================== FATURAMENTO (só dono) ====================

class FaturamentoView(generics.RetrieveAPIView):
    """
    Endpoint para listar o faturamento da empresa.
    Só pode ser acessado pelo dono (superusuário).
    """
    queryset = ResumoFinanceiro.objects.all()
    serializer_class = ResumoFinanceiroSerializer
    permission_classes = [IsAuthenticated, IsDonoPermission]

    def get_object(self):
        return ResumoFinanceiro.get_solo()


# ==================== LISTAGEM DE ESTOQUE (autenticado) ====================

class EstoqueListView(generics.ListAPIView):
    """Lista todo o estoque (apenas usuários autenticados)"""
    queryset = Estoque.objects.select_related('produto_id').all()
    serializer_class = EstoqueSerializer
    permission_classes = [IsAuthenticated]


# ==================== CATEGORIAS E MERCADORIAS (ViewSets) ====================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [p() for p in permission_classes]


class MercadoriaViewSet(viewsets.ModelViewSet):
    queryset = Mercadoria.objects.all()
    serializer_class = MercadoriaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [p() for p in permission_classes]


# ==================== VENDAS (ViewSet) ====================

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all().order_by('-data')
    serializer_class = VendaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Usuário comum vê apenas suas próprias vendas; admin vê todas"""
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Venda.objects.all().order_by('-data')
        return Venda.objects.filter(usuario_id=user).order_by('-data')


# ==================== FUNCTION BASED VIEW (FBV) - Exemplo @api_view ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meus_dados(request):
    """Retorna os dados do usuário logado"""
    user = request.user
    serializer = UsuarioSerializer(user)
    return Response(serializer.data)