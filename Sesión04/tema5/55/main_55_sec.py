# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. Lista blanca de orígenes permitidos
# NUNCA uses ["*"] en producción para endpoints que requieren autenticación.
origins = [
    "https://mi-frontend-seguro.com",
    "http://localhost:3000", # Para desarrollo local
]

# 2. Configuración del middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Especifica los orígenes permitidos
    allow_credentials=True,           # Permite cookies/tokens de autorización
    allow_methods=["GET", "POST"],    # Permite solo métodos GET y POST
    allow_headers=["Authorization"],  # Permite solo la cabecera Authorization
)

# Endpoint de ejemplo para obtener datos
@app.get("/api/data")
def get_data():
    return {"message": "¡Estos son datos seguros!"}

# Endpoint de ejemplo para enviar datos
@app.post("/api/data")
def post_data(data: dict):
    return {"message": "Datos recibidos", "received": data}