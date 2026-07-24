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


@admin.register(ResumoFinanceiro)
class ResumoFinanceiroAdmin(admin.ModelAdmin):
    list_display = ['faturamento_total']


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']


@admin.register(EtapaPipeline)
class EtapaPipelineAdmin(admin.ModelAdmin):
    list_display = ['nome', 'pipeline', 'ordem', 'probabilidade']
    list_filter = ['pipeline']
    ordering = ['pipeline', 'ordem']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'origem', 'status', 'responsavel', 'criado_em']
    list_filter = ['origem', 'status']
    search_fields = ['nome', 'email', 'telefone', 'empresa']


@admin.register(Oportunidade)
class OportunidadeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'pipeline', 'etapa', 'valor', 'status', 'responsavel', 'previsao_fechamento']
    list_filter = ['pipeline', 'etapa', 'status']
    search_fields = ['titulo']


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'usuario', 'concluida', 'data_prevista', 'criado_em']
    list_filter = ['tipo', 'concluida']
    search_fields = ['titulo', 'descricao']


@admin.register(InteracaoCliente)
class InteracaoClienteAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'canal', 'assunto', 'criado_em']
    list_filter = ['canal']
    search_fields = ['assunto', 'mensagem', 'cliente__username', 'cliente__nome']