from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView
from django.forms import modelformset_factory

from .models import CartItem, Produto
from django.contrib import messages


class CreateCartItemView(RedirectView):
    """ RedirectView requer uma url de redirecionamento"""
    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Produto, pk=self.kwargs['pk'])

# class CreateCartItemView(View):

    # def get_product(self, pk):
    #     product = Produto.objects.get(pk=pk)
        # Força a criação de uma sessão para termos cart_key
        # session_key é uma chave com caracteres que será salvo em CartItem.cart_key
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(
            self.request.session.session_key, product
        )
        # if created:
        #     messages.success(self.request, "Produto adicionado com sucesso")
        # else:
        #     messages.success(self.request, "Produto ATUALIZADO com sucesso")
        return reverse('vendas:cart_item')

create_cartitem = CreateCartItemView.as_view()


class CartItemView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        """
        Sobrescreve o que será exibido no contexto do template
        queryset será a lista dos itens do carrinho da sessão atual
        queryset=CartItem.objects.none() gera uma queryset vazia, não terá form
        """
        context = super(CartItemView, self).get_context_data(**kwargs)
        CartItemFormSet = modelformset_factory(
            CartItem, fields=('quantity',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        # Só terá session_key se tiver item (criada acima em CreateCartItemView)
        if session_key:
            context['formset'] = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key))
        else:
            context['formset'] = CartItemFormSet(queryset=CartItem.objects.none())
        return context

cart_item = CartItemView.as_view()