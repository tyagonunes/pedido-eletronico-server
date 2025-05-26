from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CategoriaViewSet, ProdutoViewSet

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('produtos', ProdutoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]