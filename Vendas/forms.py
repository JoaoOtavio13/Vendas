from django import forms
from .models import *
from django.contrib.auth.forms import UserChangeForm

class ClienteForm(forms.ModelForm):
    nome = forms.CharField(requerired=True, help_text = "Digite o nome do cliente")
    cpf = forms.CharField(required=True, help_text = "Digite o CPF do cliente")
    email = forms.EmailField(required=True, help_text = "Digite o email do cliente")
    idade = forms.IntegerField(required=True, help_text = "Digite a idade do cliente")
    cidade = forms.CharField(required=True, help_text = "Digite a cidade do cliente")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['idade'].widget.attrs.update({'class': 'form-control'})
        self.fields['cidade'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

        class Meta:
            model = Cliente
            fields = ['username', 'nome', 'email', 'idade', 'cidade', 'password1', 'password2']

class ClienteEditForm(UserChangeForm):
    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    idade = forms.IntegerField(
        required=False,
        help_text="Digite a sua idade",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    cidade = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Cliente
        fields = ['username', 'nome', 'email', 'idade', 'cidade']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']

    widgets = {
        'nome': forms.TextInput(attrs={'class': 'form-control'}),
        'descricao': forms.Textarea(attrs={'class': 'form-control'}),
    }

import django_filters

class CategoriaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Pesquisar por nome', 'class': 'form-control'}),required=False)

    class Meta:
        model = Categoria
        fields = ['nome']

class MercadoriaForm(forms.ModelForm):
    class Meta:
        model = Mercadoria
        fields = ['nome', 'categoria_id', 'descricao']

    widgets = {
        'nome': forms.TextInput(attrs={'class': 'form-control'}),
        'categoria_id': forms.Select(attrs={'class': 'form-control'}),
        'descricao': forms.Textarea(attrs={'class': 'form-control'}),
    }

class MercadoriaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Pesquisar por nome', 'class': 'form-control'}),required=False)

    class Meta:
        model = Mercadoria
        fields = ['nome']

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'mercadoria_id', 'preco']

    widgets = {
        'nome': forms.TextInput(attrs={'class': 'form-control'}),
        'mercadoria_id': forms.Select(attrs={'class': 'form-control'}),
        'preco': forms.NumberInput(attrs={'class': 'form-control'}),
    }

class ProdutoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Pesquisar por nome', 'class': 'form-control'}),required=False)

    class Meta:
        model = Produto
        fields = ['nome']

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente_id']

    widgets = {
        'cliente_id': forms.Select(attrs={'class': 'form-control'}),
    }

class VendaProdutoForm(forms.ModelForm):
    class Meta:
        model = Venda_Produto
        fields = ['venda_id', 'produto_id', 'quantidade']

    widgets = {
        'venda_id': forms.Select(attrs={'class': 'form-control'}),
        'produto_id': forms.Select(attrs={'class': 'form-control'}),
        'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
    }

class VendaProdutoFilter(django_filters.FilterSet):
    venda_id = django_filters.ModelChoiceFilter(queryset=Venda.objects.all(), label='Venda', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    produto_id = django_filters.ModelChoiceFilter(queryset=Produto.objects.all(), label='Produto', widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Venda_Produto
        fields = ['venda_id', 'produto_id']



