from django.contrib import admin
from django.utils.html import format_html
from apps.core.mixins import AuditoriaAdmin, AuditoriaAdminInline
from .models import Pedido, ItemPedido


class ItemPedidoInline(AuditoriaAdminInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',) + AuditoriaAdminInline.readonly_fields
    fields = ('produto', 'quantidade', 'preco_unitario', 'subtotal')

    def subtotal(self, obj):
        if obj.pk:
            return f'R$ {obj.subtotal:.2f}'
        return '-'
    subtotal.short_description = 'Subtotal'


@admin.register(Pedido)
class PedidoAdmin(AuditoriaAdmin):
    list_display = ('id', 'usuario', 'status', 'total_formatado', 'quantidade_items', 'forma_pagamento', 'criado_em')
    list_filter = ('status', 'forma_pagamento', 'criado_em')
    search_fields = ('id', 'usuario__first_name', 'usuario__email', 'endereco_entrega')
    readonly_fields = ('total', 'quantidade_total_items') + AuditoriaAdmin.readonly_fields
    inlines = [ItemPedidoInline]
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('usuario', 'status', 'total', 'quantidade_total_items')
        }),
        ('Entrega e Pagamento', {
            'fields': ('endereco_entrega', 'forma_pagamento', 'observacoes')
        }),
        ('Auditoria', {
            'fields': AuditoriaAdmin.readonly_fields,
            'classes': ('collapse',)
        }),
    )

    def total_formatado(self, obj):
        return f'R$ {obj.total:.2f}'
    total_formatado.short_description = 'Total'
    total_formatado.admin_order_field = 'total'

    def quantidade_items(self, obj):
        return obj.quantidade_total_items
    quantidade_items.short_description = 'Qtd. Itens'

    def get_readonly_fields(self, request, obj=None):
        # Se o pedido já foi confirmado ou enviado, torna a maioria dos campos readonly
        if obj and obj.status in ['confirmado', 'enviado', 'entregue']:
            return self.readonly_fields + ('endereco_entrega', 'forma_pagamento')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # Recalcula o total sempre que o pedido é salvo
        super().save_model(request, obj, form, change)
        obj.calcular_total()
        obj.save()


@admin.register(ItemPedido)
class ItemPedidoAdmin(AuditoriaAdmin):
    list_display = ('pedido', 'produto', 'quantidade', 'preco_unitario_formatado', 'subtotal_formatado')
    list_filter = ('pedido__status', 'produto__categoria')
    search_fields = ('pedido__id', 'produto__nome')
    readonly_fields = ('subtotal',) + AuditoriaAdmin.readonly_fields

    def preco_unitario_formatado(self, obj):
        return f'R$ {obj.preco_unitario:.2f}'
    preco_unitario_formatado.short_description = 'Preço Unitário'
    preco_unitario_formatado.admin_order_field = 'preco_unitario'

    def subtotal_formatado(self, obj):
        return f'R$ {obj.subtotal:.2f}'
    subtotal_formatado.short_description = 'Subtotal'
