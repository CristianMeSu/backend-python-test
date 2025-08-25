from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Función auxiliar para consultar la base de datos
def query_db(query, args=(), one=False):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/users", methods=["GET"])
def get_users():
    users = query_db("SELECT * FROM users")
    return jsonify([dict(row) for row in users])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
