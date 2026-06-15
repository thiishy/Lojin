import pytest
from decimal import Decimal
from models import Produto


def test_aplicar_desconto_fixo_maior_que_dez():
    produto = Produto(nome="Item Teste", preco=Decimal("50.00"))

    produto.aplicar_desconto_fixo(10.00)

    assert produto.preco == Decimal("40.00")


def test_aplicar_desconto_fixo_maior_que_o_preco_deve_lancar_erro():
    produto = Produto(nome="Item Barato", preco=Decimal("8.50"))

    with pytest.raises(
        ValueError,
        match="O valor do desconto não pode ser maior que o preço do produto.",
    ):
        produto.aplicar_desconto_fixo(10.00)


def test_aplicar_desconto_porcentagem_com_sucesso():
    produto = Produto(nome="Item Promo", preco=Decimal("200.00"))

    produto.aplicar_desconto_porcentagem(15.0)

    assert produto.preco == Decimal("170.00")


def test_aplicar_desconto_porcentagem_zero():
    produto = Produto(nome="Item Sem Promo", preco=Decimal("100.00"))

    produto.aplicar_desconto_porcentagem(0.0)

    assert produto.preco == Decimal("100.00")


def test_aplicar_desconto_porcentagem_arredondamento():
    produto = Produto(nome="Item Quebrado", preco=Decimal("33.33"))

    produto.aplicar_desconto_porcentagem(10.0)

    assert produto.preco == Decimal("30.00")
