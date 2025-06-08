from django.db import models
from django.conf import settings
from apps.core.mixins import BaseModel
from apps.produtos.models import Produto


class Pedido(BaseModel):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name='Usuário'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name='Status'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Total'
    )
    endereco_entrega = models.TextField(
        verbose_name='Endereço de Entrega'
    )
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        verbose_name='Forma de Pagamento'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )

    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.first_name}'

    @property
    def quantidade_total_items(self):
        """Retorna a quantidade total de itens no pedido."""
        return sum(item.quantidade for item in self.itens.all())

    def calcular_total(self):
        """Calcula o total do pedido baseado nos itens."""
        total = sum(item.subtotal for item in self.itens.all())
        self.total = total
        return total

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-criado_em']


class ItemPedido(BaseModel):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Pedido'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        verbose_name='Produto'
    )
    quantidade = models.PositiveIntegerField(
        verbose_name='Quantidade'
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço Unitário'
    )

    @property
    def subtotal(self):
        """Calcula o subtotal do item (quantidade * preço unitário)."""
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.produto.nome} (x{self.quantidade})'

    def save(self, *args, **kwargs):
        # Se o preço unitário não foi definido, usa o preço atual do produto
        if not self.preco_unitario:
            self.preco_unitario = self.produto.preco_promocional or self.produto.preco
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        ordering = ['id']
