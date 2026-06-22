from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .api_views import (
    RegisterView,
    ProdutoViewSet,
    CategoriaViewSet,
    MercadoriaViewSet,
    VendaViewSet,
    ProdutoDetailComEstoqueView,
    FaturamentoView,
    EstoqueListView,
    meus_dados,
)

# ==================== ROUTERS (ViewSets) ====================

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='api_produto')
router.register(r'categorias', CategoriaViewSet, basename='api_categoria')
router.register(r'mercadorias', MercadoriaViewSet, basename='api_mercadoria')
router.register(r'vendas', VendaViewSet, basename='api_venda')

# ==================== URLS DA API ====================

urlpatterns = [
    # Autenticação
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),

    # Rotas dos ViewSets (via router)
    path('', include(router.urls)),

    # Endpoints específicos
    path('produtos/<int:pk>/estoque/', ProdutoDetailComEstoqueView.as_view(), name='api_produto_estoque'),
    path('faturamento/', FaturamentoView.as_view(), name='api_faturamento'),
    path('estoque/', EstoqueListView.as_view(), name='api_estoque'),

    # FBV: dados do usuário logado
    path('meus-dados/', meus_dados, name='api_meus_dados'),
]