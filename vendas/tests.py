from django.test import TestCase

from vendas.models import Produto, Vendas
from vendas.forms import VendasForm


class ProdutoTest(TestCase):
    def setUp(self):
        Produto.objects.create(
            produto="Shorts",
            genero=2,
            total_pecas=30,
            preco_compra=25,
            preco_venda=40
        )

    def test_create(self):
        self.assertTrue(Produto.objects.exists())
        self.assertEqual(len(Produto.objects.all()), 1)


class VendasFormTest(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(
            produto="Shorts",
            genero=2,
            total_pecas=30,
            preco_compra=25,
            preco_venda=40
        )

    def test_form_has_fields(self):
        form = VendasForm()
        expected = ['status', 'valor_total_venda', 'lista_itens']
        self.assertSequenceEqual(expected, list(form.fields))


    # def test_


    # def test_registra_venda(self):
    #     lista_de_produtos = {}
    #
    #     Vendas.objects.create(
    #         status
    #     valor_total_venda
    #     lista_itens
    #     )
