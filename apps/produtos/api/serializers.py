from rest_framework import serializers
from apps.produtos.models import Categoria, Produto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'slug', 'descricao', 'ativo']



class ProdutoListSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'slug', 'preco', 'preco_promocional', 
                 'imagem', 'categoria', 'categoria_nome', 'ativo', 
                 'destaque', 'estoque']

class ProdutoDetailSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'slug', 'descricao', 'preco',
                 'preco_promocional', 'imagem', 'estoque', 'categoria',
                 'categoria_nome', 'ativo', 'destaque',
                 'criado_em', 'atualizado_em']