from rest_framework import serializers
from django.db import transaction
from apps.pedidos.models import Pedido, ItemPedido
from apps.produtos.models import Produto
from apps.produtos.api.serializers import ProdutoListSerializer


class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_detalhes = ProdutoListSerializer(source='produto', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'produto_detalhes', 
                 'quantidade', 'preco_unitario', 'subtotal']


class ItemPedidoCreateSerializer(serializers.ModelSerializer):
    produto_id = serializers.IntegerField()
    
    class Meta:
        model = ItemPedido
        fields = ['produto_id', 'quantidade', 'preco_unitario']
    
    def validate_produto_id(self, value):
        try:
            produto = Produto.objects.get(id=value, ativo=True)
        except Produto.DoesNotExist:
            raise serializers.ValidationError("Produto não encontrado ou inativo.")
        return value
    
    def validate(self, data):
        produto = Produto.objects.get(id=data['produto_id'])
        
        # Verifica se há estoque suficiente
        if data['quantidade'] > produto.estoque:
            raise serializers.ValidationError(
                f"Estoque insuficiente. Disponível: {produto.estoque}"
            )
        
        # Se o preço unitário não foi informado, usa o preço atual do produto
        if 'preco_unitario' not in data or not data['preco_unitario']:
            data['preco_unitario'] = produto.preco_promocional or produto.preco
            
        return data


class PedidoListSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.first_name', read_only=True)
    quantidade_total_items = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    forma_pagamento_display = serializers.CharField(source='get_forma_pagamento_display', read_only=True)
    
    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'usuario_nome', 'status', 'status_display',
                 'total', 'quantidade_total_items', 'forma_pagamento', 
                 'forma_pagamento_display', 'criado_em']


class PedidoDetailSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.first_name', read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)
    quantidade_total_items = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    forma_pagamento_display = serializers.CharField(source='get_forma_pagamento_display', read_only=True)
    
    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'usuario_nome', 'status', 'status_display',
                 'total', 'endereco_entrega', 'forma_pagamento', 
                 'forma_pagamento_display', 'observacoes', 'itens',
                 'quantidade_total_items', 'criado_em', 'modificado_em']


class PedidoCreateSerializer(serializers.ModelSerializer):
    items = ItemPedidoCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Pedido
        fields = ['endereco_entrega', 'forma_pagamento', 'observacoes', 'items']
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("O pedido deve conter pelo menos um item.")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        usuario = self.context['request'].user
        
        # Cria o pedido sem o total (será calculado depois)
        pedido = Pedido.objects.create(
            usuario=usuario,
            total=0,  # Temporariamente 0
            **validated_data
        )
        
        # Cria os itens do pedido e atualiza o estoque
        total_pedido = 0
        for item_data in items_data:
            produto = Produto.objects.select_for_update().get(id=item_data['produto_id'])
            
            # Verifica novamente o estoque (pode ter mudado entre a validação e criação)
            if item_data['quantidade'] > produto.estoque:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque}"
                )
            
            # Cria o item do pedido
            item_pedido = ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=item_data['quantidade'],
                preco_unitario=item_data['preco_unitario']
            )
            
            # Reduz o estoque do produto
            produto.estoque -= item_data['quantidade']
            produto.save()
            
            # Adiciona ao total do pedido
            total_pedido += item_pedido.subtotal
        
        # Atualiza o total do pedido
        pedido.total = total_pedido
        pedido.save()
        
        return pedido


class PedidoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['status', 'endereco_entrega', 'forma_pagamento', 'observacoes']
    
    def validate_status(self, value):
        instance = self.instance
        if instance and instance.status == 'cancelado':
            raise serializers.ValidationError("Não é possível alterar um pedido cancelado.")
        return value 