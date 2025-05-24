from django.urls import path, include
from apps.contas.views import GoogleLoginApi

app_name = "contas"
urlpatterns = [
    path("api/", include("apps.contas.api.urls")),
    path("login-google/", GoogleLoginApi.as_view(), name="login_google"),
]
