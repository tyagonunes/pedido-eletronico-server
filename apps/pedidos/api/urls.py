from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .viewsets import PedidoViewSet, ItemPedidoViewSet

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'itens-pedido', ItemPedidoViewSet, basename='item-pedido')

urlpatterns = [
    path('', include(router.urls)),
] 