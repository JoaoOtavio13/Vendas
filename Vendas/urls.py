from django.urls import path
from Vendas.views import *

urlpatterns = [
    path('', index, name='index'),
    path('venda/<int:venda_id>/', venda, name='venda'),
    path('cadastro_cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('editar_cliente/<int:id>/', editar_cliente, name='editar_cliente'),
    path('excluir_cliente/<int:id>/', excluir_cliente, name='excluir_cliente'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cadastro_categoria/', cadastro_categoria, name='cadastro_categoria'),
    path('editar_categoria/<int:id>/', editar_categoria, name='editar_categoria'),
    path('excluir_categoria/<int:id>/', excluir_categoria, name='excluir_categoria'),
    path('cadastro_mercadoria/', cadastro_mercadoria, name='cadastro_mercadoria'),
    path('cadastro_produto/', cadastro_produto, name='cadastro_produto'),
    path('editar_mercadoria/<int:id>/', editar_mercadoria, name='editar_mercadoria'),
    path('excluir_mercadoria/<int:id>/', excluir_mercadoria, name='excluir_mercadoria'),
    path('editar_produto/<int:id>/', editar_produto, name='editar_produto'),
    path('excluir_produto/<int:id>/', excluir_produto, name='excluir_produto'),
    path('perfil/', perfil, name='perfil'),
]