from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from apps.contas.forms import UserChangeForm, UserCreationForm
from apps.core.mixins import AuditoriaAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("Usuário", {"fields": ("papel", "metodo_registro", "foto_rede_social")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "is_superuser"]
