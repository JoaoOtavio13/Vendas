from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
import django_filters

class UsuarioForm(UserCreationForm):
    nome = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    idade = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    endereco = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    cidade = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    imagem = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['idade'].widget.attrs.update({'class': 'form-control'})
        self.fields['cpf'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefone'].widget.attrs.update({'class': 'form-control'})
        self.fields['endereco'].widget.attrs.update({'class': 'form-control'})
        self.fields['cidade'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['imagem'].widget.attrs.update({'class': 'form-control'})

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['username', 'nome', 'idade', 'cpf', 'telefone', 'endereco', 'cidade', 'email', 'imagem', 'password1', 'password2']

class UsuarioEditForm(forms.ModelForm):
    nome= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    idade = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    cpf = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    endereco = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    cidade = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    imagem = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classe fomr-control aos campos padrão
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagem'].widget.attrs.update({'class': 'form-control'})

#Formulário para criar categoria
class CategoriaForm(forms.ModelForm):
    imagem = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
        }

#Formulário para editar categoria
class CategoriaEditForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}) 
    )
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    imagem = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagem'].widget.attrs.update({'class': 'form-control'})

#Filtro para pesquisar categorias por nome
class CategoriaFilterForm(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Pesquisar por nome', 'class': 'form-control'}), required=False)

    class Meta:
        model = Categoria
        fields = ['nome']

#Formulário para criar mercadoria
class MercadoriaForm(forms.ModelForm):
    imagem = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Mercadoria
        fields = ['nome', 'categoria_id', 'descricao', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria_id': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
        }

#Formulário pata editar mercadoria
class MercadoriaEditForm(forms.ModelForm):
    nome= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    categoria_id = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    imagem = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagem'].widget.attrs.update({'class': 'form-control'})

#Filtro para pesquisar mercadorias por nome
class MercadoriaFilterForm(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Pesquisar por nome', 'class': 'form-control'}), required=False)

    class Meta:
        model = Mercadoria
        fields = ['nome']

#Formulário para criar produto
class ProdutoForm(forms.ModelForm):
    imagem = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Produto
        fields = ['nome', 'mercadoria_id', 'preco', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'mercadoria_id': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
        }

#Formulário para editar produto
class ProdutoEditForm(forms.ModelForm):
    imagem = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Produto
        fields = ['nome', 'mercadoria_id', 'preco', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'mercadoria_id': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
        }

#Filtro para pesquisar produtos por nome
class ProdutoFilterForm(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome', widget=forms.TextInput(attrs={'placeholder': 'Pesquisar por nome', 'class': 'form-control'}), required=False)

    class Meta:
        model = Produto
        fields = ['nome']


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['usuario_id']
        widgets = {
            'usuario_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_usuario_id(self):
        usuario = self.cleaned_data.get('usuario_id')
        if not usuario:
            raise forms.ValidationError('Selecione um cliente para realizar a venda.')
        return usuario


class VendaProdutoForm(forms.ModelForm):
    class Meta:
        model = Venda_Produto
        fields = ['venda_id', 'produto_id', 'quantidade']
        widgets = {
            'venda_id': forms.Select(attrs={'class': 'form-control'}),
            'produto_id': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_produto_id(self):
        produto = self.cleaned_data.get('produto_id')
        if not produto:
            raise forms.ValidationError('Selecione um produto para adicionar à venda.')
        return produto

#Filtro de compras do cliente
class VendaFilterForm(django_filters.FilterSet):
    data = django_filters.DateFromToRangeFilter(label='Data', widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Venda
        fields = ['data']


#Formulário de Estoque
class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto_id', 'quantidade', 'minimo_quantidade']
        widgets = {
            'produto_id': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'minimo_quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }
