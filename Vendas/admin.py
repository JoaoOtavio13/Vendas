from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'nome', 'email', 'is_staff']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']

@admin.register(Mercadoria)
class MercadoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome']  

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ['produto_id']    

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['usuario_id']

@admin.register(Venda_Produto)
class VendaProdutoAdmin(admin.ModelAdmin):
    list_display = ['venda_id']