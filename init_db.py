import sqlite3

rows = [
    ("2025-01-01", 6.90),
    ("2025-01-02", 6.91),
    ("2025-01-03", 6.92),
    ("2025-01-04", 6.89),
    ("2025-01-05", 6.88),
    ("2025-01-06", 6.90),
    ("2025-01-07", 6.91),
    ("2025-01-08", 6.93),
    ("2025-01-09", 6.94),
    ("2025-01-10", 6.92),
    ("2025-01-11", 6.91),
    ("2025-01-12", 6.90),
    ("2025-01-13", 6.89),
    ("2025-01-14", 6.88),
    ("2025-01-15", 6.90),
    ("2025-01-16", 6.91),
    ("2025-01-17", 6.92),
    ("2025-01-18", 6.93),
    ("2025-01-19", 6.94),
    ("2025-01-20", 6.95)
]

conn = sqlite3.connect("datos.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS tipo_cambio")
cur.execute(
    "CREATE TABLE tipo_cambio ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "fecha TEXT NOT NULL,"
    "tipo_cambio REAL NOT NULL)"
)
cur.executemany(
    "INSERT INTO tipo_cambio (fecha, tipo_cambio) VALUES (?, ?)",
    rows
)
conn.commit()
conn.close()
