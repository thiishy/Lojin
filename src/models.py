from decimal import Decimal
from database import Base
from sqlalchemy import Column, String, Integer, Numeric


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String(64), nullable=False)
    descricao = Column(String(256))
    preco = Column(Numeric(precision=10, scale=2), nullable=False)

    def aplicar_desconto_porcentagem(self, valor_porcentagem: float) -> None:
        porcentagem = Decimal(str(valor_porcentagem))
        self.preco = round(self.preco * (1 - porcentagem / 100), 2)

    def aplicar_desconto_fixo(self, valor_fixo: float) -> None:
        desconto = Decimal(str(valor_fixo))

        if desconto > self.preco:
            raise ValueError(
                "O valor do desconto não pode ser maior que o preço do produto."
            )

        self.preco = round(self.preco - desconto, 2)
