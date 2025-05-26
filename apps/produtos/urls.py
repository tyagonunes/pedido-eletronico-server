from django.urls import path, include

app_name = "produtos"
urlpatterns = [
    path('api/', include('apps.produtos.api.urls')),
]