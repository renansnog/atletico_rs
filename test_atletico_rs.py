"""Testes de integração locais. Execute com o MySQL configurado no .env."""
from uuid import uuid4
from unittest.mock import patch

import mysql.connector
import pytest
from app import app, banco


@pytest.fixture
def client():
    with app.test_client() as c:
        yield c


@pytest.fixture
def jogador(client):
    dados = {"nome": "Teste " + uuid4().hex, "idade": 25}
    r = client.post("/api/jogadores", json=dados)
    assert r.status_code == 201, r.get_json()
    ident = r.get_json()["id"]
    try:
        yield ident, dados
    finally:
        r = client.delete(f"/api/jogadores/{ident}")
        assert r.status_code in (204, 404)


def test_pagina(client):
    assert client.get("/").status_code == 200


def test_conexao_mysql():
    with banco() as cursor:
        cursor.execute("SELECT 1 AS ok")
        assert cursor.fetchone()["ok"] == 1


def test_cadastro_e_consulta(client, jogador):
    ident, dados = jogador
    r = client.get(f"/api/jogadores/{ident}")
    assert r.status_code == 200
    assert r.get_json()["nome"] == dados["nome"]
    assert r.get_json()["idade"] == 25
    r = client.get("/api/jogadores")
    assert r.status_code == 200
    assert any(j["id"] == ident for j in r.get_json())


def test_edicao(client, jogador):
    ident, dados = jogador
    assert client.put(f"/api/jogadores/{ident}", json={**dados, "idade": 26}).status_code == 204
    r = client.get(f"/api/jogadores/{ident}")
    assert r.status_code == 200
    assert r.get_json()["idade"] == 26


def test_exclusao(client, jogador):
    ident, _ = jogador
    assert client.delete(f"/api/jogadores/{ident}").status_code == 204
    assert client.get(f"/api/jogadores/{ident}").status_code == 404


def test_agenda(client):
    dados = {"adversario": "Teste " + uuid4().hex, "local": "Estadio teste",
             "data": "2026-12-30", "horario": "16:00"}
    r = client.post("/api/agenda", json=dados)
    assert r.status_code == 201, r.get_json()
    ident = r.get_json()["id"]
    try:
        r = client.get("/api/agenda")
        assert r.status_code == 200
        partida = next(p for p in r.get_json() if p["id"] == ident)
        assert partida["adversario"] == dados["adversario"]
        assert partida["local"] == dados["local"]
        assert partida["data"] == dados["data"]
        assert partida["horario"].startswith(dados["horario"])
    finally:
        with banco() as cursor:
            cursor.execute("DELETE FROM agenda WHERE id = %s AND adversario = %s",
                           (ident, dados["adversario"]))


def test_diretoria(client):
    r = client.get("/api/diretoria")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)


@pytest.mark.parametrize("dados", [{"nome": "", "idade": 25},
                                  {"nome": "Teste", "idade": -1},
                                  {"nome": "Teste", "idade": "25"},
                                  {"nome": "Teste", "idade": 25, "foto": "invalida.png"}])
def test_jogador_invalido(client, dados):
    assert client.post("/api/jogadores", json=dados).status_code == 400


def test_partida_invalida(client):
    assert client.post("/api/agenda", json={"adversario": "Teste", "local": "Teste",
                       "data": "2026-02-30", "horario": "16:00"}).status_code == 400


def test_erro_mysql_simulado(client):
    with patch("app.mysql.connector.connect", side_effect=mysql.connector.Error(errno=1045)):
        r = client.get("/api/jogadores")
        assert r.status_code == 503
        assert "erro" in r.get_json()
