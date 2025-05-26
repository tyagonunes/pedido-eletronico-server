from rest_framework import viewsets, permissions, filters, status
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters_drf
from apps.produtos.models import Categoria, Produto
from .serializers import (
    CategoriaSerializer, 
    ProdutoListSerializer, 
    ProdutoDetailSerializer,
)


class ProdutoFilter(django_filters.FilterSet):
    preco_min = django_filters.NumberFilter(field_name="preco", lookup_expr='gte')
    preco_max = django_filters.NumberFilter(field_name="preco", lookup_expr='lte')
    categoria = django_filters.CharFilter(field_name="categoria__slug")
    categoria_ids = django_filters.BaseInFilter(field_name="categoria__id")
    destaque = django_filters.BooleanFilter(field_name="destaque")
    
    class Meta:
        model = Produto
        fields = ['categoria', 'categoria_ids', 'destaque', 'preco_min', 'preco_max']

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.filter(ativo=True)
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'descricao']
    lookup_field = 'slug'

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.filter(ativo=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProdutoFilter
    search_fields = ['nome', 'descricao', 'categoria__nome']
    ordering_fields = ['nome', 'preco', 'criado_em']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProdutoListSerializer
        return ProdutoDetailSerializer
    
    