from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.pedidos.models import Pedido, ItemPedido
from .serializers import (
    PedidoListSerializer,
    PedidoDetailSerializer,
    PedidoCreateSerializer,
    PedidoUpdateSerializer,
    ItemPedidoSerializer
)


class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'forma_pagamento']
    search_fields = ['id', 'endereco_entrega']
    ordering_fields = ['criado_em', 'total', 'status']
    ordering = ['-criado_em']

    def get_queryset(self):
        """Retorna apenas os pedidos do usuário logado."""
        return Pedido.objects.filter(usuario=self.request.user).prefetch_related('itens__produto')

    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoListSerializer
        elif self.action == 'create':
            return PedidoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PedidoUpdateSerializer
        else:
            return PedidoDetailSerializer

    def create(self, request, *args, **kwargs):
        """Cria um novo pedido."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            pedido = serializer.save()
            response_serializer = PedidoDetailSerializer(pedido)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """Atualiza um pedido."""
        instance = self.get_object()
        
        # Verifica se o usuário pode atualizar este pedido
        if instance.usuario != request.user:
            return Response(
                {'error': 'Você não tem permissão para editar este pedido.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Não permite atualizar pedidos cancelados
        if instance.status == 'cancelado':
            return Response(
                {'error': 'Não é possível atualizar um pedido cancelado.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def cancelar(self, request, pk=None):
        """Cancela um pedido e restaura o estoque."""
        pedido = self.get_object()
        
        if pedido.usuario != request.user:
            return Response(
                {'error': 'Você não tem permissão para cancelar este pedido.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if pedido.status == 'cancelado':
            return Response(
                {'error': 'Este pedido já está cancelado.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if pedido.status in ['enviado', 'entregue']:
            return Response(
                {'error': 'Não é possível cancelar um pedido que já foi enviado ou entregue.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancela o pedido e restaura o estoque
        with transaction.atomic():
            for item in pedido.itens.all():
                produto = item.produto
                produto.estoque += item.quantidade
                produto.save()
            
            pedido.status = 'cancelado'
            pedido.save()
        
        serializer = PedidoDetailSerializer(pedido)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def meus_pedidos(self, request):
        """Retorna todos os pedidos do usuário logado."""
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PedidoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PedidoListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos pedidos do usuário."""
        queryset = self.get_queryset()
        
        total_pedidos = queryset.count()
        total_gasto = sum(pedido.total for pedido in queryset)
        
        pedidos_por_status = {}
        for status_choice in Pedido.STATUS_CHOICES:
            status_value = status_choice[0]
            count = queryset.filter(status=status_value).count()
            pedidos_por_status[status_value] = count
        
        return Response({
            'total_pedidos': total_pedidos,
            'total_gasto': total_gasto,
            'pedidos_por_status': pedidos_por_status
        })


class ItemPedidoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet apenas para leitura dos itens de pedido."""
    serializer_class = ItemPedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['pedido', 'produto']
    search_fields = ['produto__nome']

    def get_queryset(self):
        """Retorna apenas os itens dos pedidos do usuário logado."""
        return ItemPedido.objects.filter(
            pedido__usuario=self.request.user
        ).select_related('produto', 'pedido') 