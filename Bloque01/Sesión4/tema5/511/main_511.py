import time
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 1. Crear una instancia del limitador.
#    Utiliza la dirección IP del cliente como identificador único.
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# 2. Registrar el manejador de excepciones y el middleware del limitador en la app.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 3. Aplicar un límite a un endpoint específico usando un decorador.
#    Este endpoint solo permite 5 peticiones por minuto.
@app.get("/items")
@limiter.limit("5/minute")
async def list_items(request: Request):
    return {"data": ["item1", "item2", "item3"]}

# 4. Aplicar un límite más estricto a un endpoint más sensible.
#    Este endpoint de login solo permite 10 peticiones por hora para proteger contra fuerza bruta.
@app.get("/login")
@limiter.limit("10/hour")
async def login(request: Request):
    return {"message": "Login endpoint"}