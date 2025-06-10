import sqlite3

def init_db():
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id TEXT, name TEXT, price REAL)")
    cursor.execute("INSERT INTO items VALUES ('1', 'InsecureProduct', 99.99)")
    cursor.execute("INSERT INTO items VALUES ('2', 'Otro', 49.99)")
    cursor.execute("INSERT INTO items VALUES ('3', 'Más', 9.99)")

    conn.commit()
    conn.close()