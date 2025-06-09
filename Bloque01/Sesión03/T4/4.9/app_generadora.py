# app_generadora.py
import time
import logging
import json
from fastapi import FastAPI, HTTPException, Request

# --- Configuración del Logger para escribir a un fichero en formato JSON ---
log_file = "api_logs.log"
handler = logging.FileHandler(log_file)
# No usamos un formatter complejo, escribiremos el JSON directamente.

logger = logging.getLogger('api_logger')
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False
# -------------------------------------------------------------

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # en milisegundos

    log_entry = {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "status_code": response.status_code,
        "latency_ms": process_time,
        "path": request.url.path
    }
    logger.info(json.dumps(log_entry))
    return response

@app.get("/")
def endpoint_exitoso():
    return {"status": "ok"}

@app.get("/lento")
async def endpoint_lento():
    import asyncio
    await asyncio.sleep(1.5)
    return {"status": "ok, pero lento"}

@app.get("/error-cliente")
def endpoint_error_cliente():
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Recurso no encontrado")

@app.get("/error-servidor")
def endpoint_error_servidor():
    raise HTTPException(status_code=501, detail="Error Servidor")