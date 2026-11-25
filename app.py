import os
from contextlib import contextmanager
from datetime import date, time

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()
app = Flask(__name__)
app.config["TRUSTED_HOSTS"] = ["127.0.0.1", "localhost"]

FOTOS = {"leonelMessi.png", "carlosAndrade.png", "andreVieira.png", "paulinhoSabia.png"}


@contextmanager
def banco():
    with mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "atletico_app"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "atletico_rs"),
        connection_timeout=5,
    ) as conexao:
        with conexao.cursor(dictionary=True) as cursor:
            yield cursor
            conexao.commit()


@app.errorhandler(mysql.connector.Error)
def erro_banco(erro):
    app.logger.error("Falha no MySQL (código %s)", erro.errno)
    return jsonify(erro="Banco de dados indisponível. Confira a configuração e tente novamente."), 503


@app.errorhandler(ValueError)
def dados_invalidos(erro):
    return jsonify(erro=str(erro)), 400


def dados_json():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ValueError("Envie os dados como um objeto JSON.")
    return dados


def campo_texto(dados, chave, rotulo, limite, obrigatorio=True):
    valor = dados.get(chave, "")
    if not isinstance(valor, str):
        raise ValueError(f"{rotulo} deve ser um texto.")
    valor = valor.strip()
    if len(valor) > limite or (obrigatorio and not valor):
        raise ValueError(f"{rotulo} deve ter entre {int(obrigatorio)} e {limite} caracteres.")
    return valor


def dados_jogador():
    dados = dados_json()
    nome = campo_texto(dados, "nome", "Nome", 100)
    idade = dados.get("idade")
    if type(idade) is not int or not 1 <= idade <= 120:
        raise ValueError("Informe uma idade inteira de 1 a 120 anos.")
    nascimento = campo_texto(dados, "localNascimento", "Local de nascimento", 100, False)
    times = campo_texto(dados, "timesAnterior", "Times anteriores", 300, False)
    foto = campo_texto(dados, "foto", "Foto", 200, False)
    if foto and foto not in FOTOS:
        raise ValueError("Escolha uma das fotos disponíveis.")
    return nome, idade, nascimento, times, foto


@app.get("/")
def home():
    return app.send_static_file("index.html")


@app.route("/api/jogadores", methods=["GET", "POST"])
def jogadores():
    if request.method in ("GET", "HEAD"):
        with banco() as cursor:
            cursor.execute("SELECT * FROM jogadores ORDER BY nome, id")
            return jsonify(cursor.fetchall())

    dados = dados_jogador()
    with banco() as cursor:
        cursor.execute(
            """INSERT INTO jogadores (nome, idade, localNascimento, timesAnterior, foto)
               VALUES (%s, %s, %s, %s, %s)""",
            dados,
        )
        jogador_id = cursor.lastrowid
    return jsonify(id=jogador_id), 201


@app.route("/api/jogadores/<int:jogador_id>", methods=["GET", "PUT", "DELETE"])
def jogador(jogador_id):
    dados = dados_jogador() if request.method == "PUT" else None
    with banco() as cursor:
        consulta = "SELECT * FROM jogadores WHERE id = %s"
        if request.method in ("PUT", "DELETE"):
            consulta += " FOR UPDATE"
        cursor.execute(consulta, (jogador_id,))
        registro = cursor.fetchone()
        if registro is None:
            return jsonify(erro="Jogador não encontrado."), 404
        if request.method in ("GET", "HEAD"):
            return jsonify(registro)
        if request.method == "PUT":
            cursor.execute(
                """UPDATE jogadores SET nome = %s, idade = %s, localNascimento = %s,
                   timesAnterior = %s, foto = %s WHERE id = %s""",
                (*dados, jogador_id),
            )
        else:
            cursor.execute("DELETE FROM jogadores WHERE id = %s", (jogador_id,))
    return "", 204


@app.route("/api/agenda", methods=["GET", "POST"])
def agenda():
    if request.method in ("GET", "HEAD"):
        with banco() as cursor:
            cursor.execute(
                """SELECT id, CAST(data AS CHAR) AS data,
                          CAST(horario AS CHAR) AS horario, local, adversario
                   FROM agenda ORDER BY data, horario, id"""
            )
            return jsonify(cursor.fetchall())

    dados = dados_json()
    local = campo_texto(dados, "local", "Local", 200)
    adversario = campo_texto(dados, "adversario", "Adversário", 100)
    data = campo_texto(dados, "data", "Data", 10)
    horario = campo_texto(dados, "horario", "Horário", 5)
    try:
        dia = date.fromisoformat(data)
        hora = time.fromisoformat(horario)
        if dia.year < 1000 or dia.isoformat() != data or hora.isoformat(timespec="minutes") != horario:
            raise ValueError
    except ValueError:
        raise ValueError("Informe a data como AAAA-MM-DD e a hora como HH:MM.") from None
    with banco() as cursor:
        cursor.execute(
            "INSERT INTO agenda (data, horario, local, adversario) VALUES (%s, %s, %s, %s)",
            (data, horario, local, adversario),
        )
        partida_id = cursor.lastrowid
    return jsonify(id=partida_id), 201


@app.get("/api/diretoria")
def diretoria():
    with banco() as cursor:
        cursor.execute("SELECT * FROM diretoria ORDER BY id")
        return jsonify(cursor.fetchall())


if __name__ == "__main__":
    app.run(host="127.0.0.1")
