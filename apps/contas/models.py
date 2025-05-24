from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings 
from apps.contas.choices import *
from apps.core.mixins import BaseModel

class User(AbstractUser):
    papel = models.IntegerField('Papel', choices=CHOICES_USER_PAPEL, default=USER_PAPEL_CLIENTE)
    email = models.CharField(max_length=250, unique=True, null=False, blank=False)
    metodo_registro = models.IntegerField(choices=CHOICES_METODO_REGISTRO, default=METODO_REGISTRO_EMAIL)
    foto_rede_social = models.URLField('Foto rede social', blank=True, null=True)

    def is_distribuidora(self):
        """Verifica se o usuário tem papel de distribuidora."""
        return self.papel == USER_PAPEL_DISTRIBUIDORA

    def is_cliente(self):
        """Verifica se o usuário tem papel de cliente."""
        return self.papel == USER_PAPEL_CLIENTE
    
    def __str__(self):
        return str(self.username)

    # pylint: disable=too-few-public-methods
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    from datetime import datetime, timedelta

    data_expiracao = datetime.now() + timedelta(hours=1)

    dados = {
        'nome': reset_password_token.user.first_name,
        'token': reset_password_token.key,
        'data_expiracao': data_expiracao.strftime('%d/%m/%Y às %H:%M'),
    }

    subject = "Codigo para recuperação de senha"
    message = f'{dados["nome"]} o seu codigo para recuperação de senha é {dados["token"]}. Esse codigo expira em {dados["data_expiracao"]}'
    recipient_list = [reset_password_token.user.email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)