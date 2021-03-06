from django.conf import settings
from django.db import models


class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            return val.isoformat()
        return ''


generos = (
    (1, "Masculino"),
    (2, "Feminino")
)

class Produto(models.Model):
    produto = models.CharField("Produto", max_length=50)
    genero = models.SmallIntegerField("Gênero", choices=generos, default=1)
    total_pecas = models.PositiveSmallIntegerField("Total de Peças")
    preco_compra = models.DecimalField("Preço de Compra", max_digits=6, decimal_places=2)
    preco_venda = models.DecimalField("Preço de Venda", max_digits=6, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    # criado_em = CustomDateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.produto


VENDAS_STATUS = (
    (1, 'Pendente'),
    (2, 'Cancelada'),
    (3, 'Concluída'),
)


class CartItemManager(models.Manager):
    def add_item(self, cart_key, product):
        """
        Se não existir o produto no carrinho, adiciona
        Se existir, atualiza a quantidade
        get_or_create retorna dois valores:
            object: item criado ou resgatado
            bool: criou ou não
        """
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity += 1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(cart_key=cart_key, product=product, price=product.preco_venda)
        # cart_item, created = self.get_or_create(cart_key=cart_key, product=product)
        return cart_item, created


class CartItem(models.Model):
    cart_key = models.CharField('Chave do Carrinho', max_length=40, db_index=True)
    product = models.ForeignKey('vendas.Produto', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    objects = CartItemManager()

    class Meta:
        verbose_name = "Item do carrinho"
        verbose_name_plural = "Itens do carrinho"
        unique_together = (('cart_key', 'product'),)

    def __str__(self):
        return f'{self.product} [{self.quantity}]'





# class Vendas(models.Model):
#     status = models.PositiveSmallIntegerField('Status', choices=VENDAS_STATUS, default='Pendente')
#     criado_em = models.DateTimeField(auto_now_add=True)
#     # criado_em = CustomDateTimeField(auto_now_add=True)
#     valor_total_venda = models.DecimalField('Valor Total da Venda', decimal_places=2, max_digits=12, default=0)
#     lista_itens = models.JSONField("Lista de Itens")
#
#     class Meta:
#         verbose_name = "Venda"
#         verbose_name_plural = "Vendas"
#
#     def __str__(self):
#         return f"{self.criado_em.strftime('%d/%m/%Y %H:%M:%S')} - {self.id}"

