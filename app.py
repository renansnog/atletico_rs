from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__, static_folder="static", template_folder="templates")

# Conexão com MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # seu usuário MySQL
        password="",      # sua senha MySQL
        database="atletico_rs"
    )

# Rota principal -> abre index.html
@app.route("/")
def home():
    return app.send_static_file("index.html")

# API Jogadores
@app.route("/api/jogadores")
def jogadores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jogadores")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

# API Agenda
@app.route("/api/agenda")
def agenda():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agenda")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

# API Diretoria
@app.route("/api/diretoria")
def diretoria():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM diretoria")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
