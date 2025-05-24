from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.forms import Textarea
from django_currentuser.middleware import get_current_user
    
class BaseModel(models.Model):
    criado_em = models.DateTimeField(blank=True, null=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_criado_por',
        blank=True,
        null=True,
        default=get_current_user()
    )
    modificado_em = models.DateTimeField(blank=True, null=True)
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_modificado_por',
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if get_current_user():
            if (not self.criado_por or not self.criado_em) and get_current_user() and get_current_user().id:
                self.criado_por = get_current_user()
                self.criado_em = timezone.now()
            elif get_current_user() and get_current_user().id:
                self.modificado_por = get_current_user()
                self.modificado_em = timezone.now()
        super(BaseModel, self).save(force_insert=False, force_update=False, using=None, update_fields=None)



class AuditoriaAdmin(admin.ModelAdmin):

    readonly_fields = (
        'criado_em',
        'criado_por',
        'modificado_em',
        'modificado_por',
    )
    list_per_page = 10


class AuditoriaAdminInline(admin.TabularInline):
    readonly_fields = (
        'criado_em',
        'criado_por',
        'modificado_em',
        'modificado_por',
    )
    list_per_page = 10
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 8,
                'cols': 40
            })
        },
        models.ForeignKey: {
            # 'widget': Select(attrs={'style': 'max-width: 150px'})
        },
        models.CharField: {
            # 'widget': TextInput(attrs={'style': 'max-width: 150px'})
        },
    }
