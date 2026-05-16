from django.db import models, transaction
from django.core.exceptions import ValidationError

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    idade = models.IntegerField()
    cidade = models.CharField(max_length=100)
   
    def __str__(self):
        return self.nome
    
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
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    minimo_quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"        
    
    
class Venda(models.Model):
    cliente_id = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())
    
    def __str__(self):
        return f"Venda #{self.id} - {self.cliente_id.nome}"
    
class Venda_Produto(models.Model):
    venda_id = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto_id = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    def subtotal(self):
        return self.produto_id.preco * self.quantidade
    
    def save(self, *args, **kwargs):
        # calcula diferença entre quantidade nova e antiga
        if self.pk:
            item_antigo = Venda_Produto.objects.get(pk=self.pk)
            diferenca = self.quantidade - item_antigo.quantidade
        else:
            diferenca = self.quantidade

        # operação transacional para evitar race conditions
        with transaction.atomic():
            estoque, created = Estoque.objects.select_for_update().get_or_create(
                produto=self.produto_id,
                defaults={'quantidade': 0, 'minimo_quantidade': 0}
            )
            novo_saldo = estoque.quantidade - diferenca
            if novo_saldo < 0:
                raise ValidationError("Estoque insuficiente para este produto.")

            super().save(*args, **kwargs)

            estoque.quantidade = novo_saldo
            estoque.save()

    def __str__(self):
        return f"Sua compra de {self.produto_id.nome} - {self.quantidade}" + f" - Totalizou: R${self.subtotal():.2f}"