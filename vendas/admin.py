from django.contrib import admin

# Register your models here.
from vendas.models import Produto, CartItem  # , Vendas


# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product', 'quantity']
#
#
# class ProdutoAdmin(admin.ModelAdmin):
#     list_display = ['id', 'produto']
#
# admin.site.register(Produto, ProdutoAdmin)
# admin.site.register(CartItem, CartItemAdmin)

# admin.site.register(Vendas)
admin.site.register(Produto)
admin.site.register(CartItem)
