from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect("datos.db")
    cur = conn.cursor()
    cur.execute("SELECT fecha, tipo_cambio FROM tipo_cambio ORDER BY fecha")
    rows = cur.fetchall()
    conn.close()
    puntos = []
    for fecha, valor in rows:
        puntos.append({"x": fecha, "y": valor})
    return puntos

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(get_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8443, ssl_context=("server.crt", "server.key"))
