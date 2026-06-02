from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    nome = models.CharField(max_length=100, blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
 
    def __str__(self):
        # Ensure __str__ always returns a string (fallback to username)
        return self.nome or self.username or ''

# Backwards-compatibility alias for migrations that referenced `User`
User = Usuario
    
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
   
    def __str__(self):
        return self.nome

class Mercadoria(models.Model):
    nome = models.CharField(max_length=100)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descricao = models.TextField()

    def __str__(self):
        return self.nome   

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    mercadoria_id = models.ForeignKey(Mercadoria, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome
    
class Estoque(models.Model):
    produto_id = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    minimo_quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.produto_id.nome} - {self.quantidade}"        


class ResumoFinanceiro(models.Model):
    faturamento_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1, defaults={'faturamento_total': 0})
        if created:
            obj.save()
        return obj

    def adicionar(self, valor):
        self.faturamento_total += valor
        self.save(update_fields=['faturamento_total'])

    def subtrair(self, valor):
        self.faturamento_total -= valor
        if self.faturamento_total < 0:
            self.faturamento_total = 0
        self.save(update_fields=['faturamento_total'])
    
    
class Venda(models.Model):
    # Campo historicamente chamado 'cliente_id' no DB; mapear para a coluna existente
    usuario_id = models.ForeignKey(Usuario, on_delete = models.CASCADE, db_column='cliente_id_id')
    data = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())
    
    def __str__(self):
        return f"Venda #{self.id} - {self.usuario_id.nome or self.usuario_id.username}"
    
class Venda_Produto(models.Model):
    venda_id = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE, db_column='venda_id_id')
    produto_id = models.ForeignKey(Produto, on_delete=models.CASCADE, db_column='produto_id_id')
    quantidade = models.IntegerField()

    def subtotal(self):
        return self.produto_id.preco * self.quantidade

    def _atualizar_faturamento(self, diferenca_valor):
        resumo = ResumoFinanceiro.get_solo()
        if diferenca_valor >= 0:
            resumo.adicionar(diferenca_valor)
        else:
            resumo.subtrair(abs(diferenca_valor))
    
    def save(self, *args, **kwargs):
        # calcula diferença entre quantidade nova e antiga
        subtotal_antigo = 0
        if self.pk:
            item_antigo = Venda_Produto.objects.get(pk=self.pk)
            diferenca = self.quantidade - item_antigo.quantidade
            subtotal_antigo = item_antigo.subtotal()
        else:
            diferenca = self.quantidade

        # operação transacional para evitar race conditions
        with transaction.atomic():
            # Estoque model uses field `produto_id`, so lookup by that field name
            estoque, created = Estoque.objects.select_for_update().get_or_create(
                produto_id=self.produto_id,
                defaults={'quantidade': 0, 'minimo_quantidade': 0}
            )
            novo_saldo = estoque.quantidade - diferenca
            if novo_saldo < 0:
                raise ValidationError("Estoque insuficiente para este produto.")

            super().save(*args, **kwargs)

            estoque.quantidade = novo_saldo
            estoque.save()

            subtotal_novo = self.subtotal()
            self._atualizar_faturamento(subtotal_novo - subtotal_antigo)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            estoque, created = Estoque.objects.select_for_update().get_or_create(
                produto_id=self.produto_id,
                defaults={'quantidade': 0, 'minimo_quantidade': 0}
            )
            estoque.quantidade += self.quantidade
            estoque.save()

            resumo = ResumoFinanceiro.get_solo()
            resumo.subtrair(self.subtotal())
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"Sua compra de {self.produto_id.nome} - {self.quantidade}" + f" - Totalizou: R${self.subtotal():.2f}"