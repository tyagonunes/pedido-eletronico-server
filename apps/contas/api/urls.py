from rest_framework.routers import DefaultRouter
from apps.contas.api.viewsets import *


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = router.urls
