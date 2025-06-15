from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.models import Item
import sqlite3

app = FastAPI()

# CORS totalmente abierto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API insegura"}

@app.get("/item-injection/{item_id}")
def read_item_injection(item_id: str):
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM items WHERE id = '{item_id}'"
    result = cursor.execute(query).fetchall()
    conn.close()
    return {"items": result}
