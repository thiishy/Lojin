import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
import models

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_criar_produto():
    dados_produto = {"nome": "Smartphone", "descricao": "5G", "preco": 2000.00}

    response = client.post("/api/v1/produtos", json=dados_produto)

    assert response.status_code == status.HTTP_201_CREATED

    dados_retornados = response.json()
    assert "id" in dados_retornados
    assert dados_retornados["id"] is not None
    assert dados_retornados["nome"] == dados_produto["nome"]
    assert dados_retornados["descricao"] == dados_produto["descricao"]
    assert dados_retornados["preco"] == dados_produto["preco"]


def test_buscar_produto():
    db = TestingSessionLocal()
    produto_fake = models.Produto(
        id=10, nome="Televisão", descricao="Smart TV", preco=2999.99
    )
    db.add(produto_fake)
    db.commit()

    id_produto = produto_fake.id
    db.close()

    response = client.get(f"/api/v1/produtos/{id_produto}")

    assert response.status_code == status.HTTP_200_OK

    dados_retornados = response.json()
    assert dados_retornados["id"] == 10
    assert dados_retornados["nome"] == "Televisão"


def test_atualizar_produto():
    db = TestingSessionLocal()
    produto_fake = models.Produto(
        id=20, nome="Monitor Antigo", descricao="60Hz", preco=500.00
    )
    db.add(produto_fake)
    db.commit()

    id_produto = produto_fake.id
    db.close()

    dados_atualizados = {
        "nome": "Monitor Gamer",
        "descricao": "144Hz IPS Ultrawide",
        "preco": 1299.90,
    }

    response = client.put(f"/api/v1/produtos/{id_produto}", json=dados_atualizados)

    assert response.status_code == status.HTTP_200_OK

    dados_retornados = response.json()
    assert dados_retornados["id"] == 20
    assert dados_retornados["nome"] == dados_atualizados["nome"]
    assert dados_retornados["descricao"] == dados_atualizados["descricao"]
    assert dados_retornados["preco"] == dados_atualizados["preco"]


def test_deletar_produto():
    db = TestingSessionLocal()
    produto_fake = models.Produto(
        id=30, nome="Produto descartável", descricao="Vai sumir", preco=10.0
    )
    db.add(produto_fake)
    db.commit()

    id_produto = produto_fake.id
    db.close()

    response = client.delete(f"/api/v1/produtos/{id_produto}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    db = TestingSessionLocal()
    produto_no_banco = db.get(models.Produto, id_produto)
    db.close()

    assert produto_no_banco is None
