from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    nome: str = Field(min_length=2, max_length=64)
    descricao: str | None = Field(default=None, max_length=256)
    preco: float

    class Config:
        orm_mode = True


class CriarProduto(ProdutoBase):
    class Config:
        orm_mode = True


class ListarProduto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True
