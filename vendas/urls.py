from django.urls import path
from .views import cart_item, create_cartitem

app_name = 'vendas'
urlpatterns = [
    path('carrinho/', cart_item, name='cart_item'),
    path('carrinho/adicionar/<int:pk>/', create_cartitem, name='create_cartitem')
]
