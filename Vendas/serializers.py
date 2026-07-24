from rest_framework import serializers
from .models import (
    Usuario,
    Categoria,
    Mercadoria,
    Produto,
    Estoque,
    ResumoFinanceiro,
    Venda,
    Venda_Produto,
    Pipeline,
    EtapaPipeline,
    Lead,
    Oportunidade,
    Atividade,
    InteracaoCliente,
)


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nome', 'email', 'password', 'password2',
                  'idade', 'cpf', 'telefone', 'endereco', 'cidade', 'imagem']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não conferem."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class MercadoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mercadoria
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'


class EstoqueSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto_id.nome', read_only=True)

    class Meta:
        model = Estoque
        fields = ['id', 'produto_id', 'produto_nome', 'quantidade', 'minimo_quantidade']


class ProdutoComEstoqueSerializer(serializers.ModelSerializer):
    estoque = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'mercadoria_id', 'preco', 'imagem', 'estoque']

    def get_estoque(self, obj):
        try:
            estoque = Estoque.objects.get(produto_id=obj)
            return EstoqueSerializer(estoque).data
        except Estoque.DoesNotExist:
            return None


class ResumoFinanceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumoFinanceiro
        fields = ['id', 'faturamento_total']


class VendaProdutoSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Venda_Produto
        fields = ['id', 'venda_id', 'produto_id', 'quantidade', 'subtotal']


class VendaSerializer(serializers.ModelSerializer):
    itens = VendaProdutoSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    usuario_nome = serializers.CharField(source='usuario_id.nome', read_only=True)

    class Meta:
        model = Venda
        fields = ['id', 'usuario_id', 'usuario_nome', 'data', 'status', 'total', 'itens']


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = '__all__'


class EtapaPipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapaPipeline
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class OportunidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oportunidade
        fields = '__all__'


class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = '__all__'


class InteracaoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteracaoCliente
        fields = '__all__'