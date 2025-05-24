from rest_framework.viewsets import ModelViewSet
from apps.contas.models import *
from apps.contas.api.serializers import *

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()
    http_method_names = ['get', 'post', 'delete', 'put', 'patch', 'head']
