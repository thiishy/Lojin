from typing import List
from fastapi import HTTPException, Depends, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api/v1/produtos", tags=["Produtos"])


@router.get("/versao")
def versao_lojin():
    return {"versao": "v1.0"}


@router.get("/", response_model=List[schemas.ListarProduto])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.scalars(select(models.Produto)).all()

    return produtos


@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.ListarProduto)
def criar_produto(produto: schemas.CriarProduto, db: Session = Depends(get_db)):
    novo_produto = models.Produto(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("/{id}", status_code=HTTP_200_OK, response_model=schemas.ListarProduto)
def buscar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, id)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O produto com o ID {id} não existe.",
        )

    return produto


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def deletar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, id)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O produto com o ID {id} não existe.",
        )

    db.delete(produto)
    db.commit()


@router.put("/{id}", response_model=schemas.ListarProduto)
def atualizar_produto(
    id: int, produto: schemas.CriarProduto, db: Session = Depends(get_db)
):
    produto_existente = db.get(models.Produto, id)

    if not produto_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O produto com o ID {id} não existe.",
        )

    produto_existente.nome = produto.nome
    produto_existente.descricao = produto.descricao
    produto_existente.preco = produto.preco

    db.commit()
    db.refresh(produto_existente)

    return produto_existente


@router.patch("/{id}/desconto-porcentagem", response_model=schemas.ListarProduto)
def aplicar_desconto_porcentagem(
    id: int, valor: float = Query(..., gt=0, le=100), db: Session = Depends(get_db)
):
    produto = db.get(models.Produto, id)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O produto com o ID {id} não existe.",
        )

    produto.aplicar_desconto_porcentagem(valor)
    db.commit()
    db.refresh(produto)

    return produto


@router.patch("/{id}/desconto-fixo", response_model=schemas.ListarProduto)
def aplicar_desconto_fixo(
    id: int, valor: float = Query(..., gt=0), db: Session = Depends(get_db)
):
    produto = db.get(models.Produto, id)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O produto com o ID {id} não existe.",
        )

    try:
        produto.aplicar_desconto_fixo(valor)
        db.commit()
        db.refresh(produto)

        return produto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
