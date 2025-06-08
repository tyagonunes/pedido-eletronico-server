from django.urls import path, include

app_name = 'pedidos'

urlpatterns = [
    path('api/', include('apps.pedidos.api.urls')),
] 