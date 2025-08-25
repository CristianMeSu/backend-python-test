import sqlite3

# Conectar (si no existe, crea el archivo database.db)
conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Crear tabla
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

# Insertar datos de prueba
cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Cristian", "cristian@email.com"))
cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Roronoa", "roronoa@email.com"))

conn.commit()
conn.close()

print("Base de datos creada y poblada con éxito 🚀")
