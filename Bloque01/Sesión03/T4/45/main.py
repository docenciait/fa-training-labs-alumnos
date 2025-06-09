# retry_client.py
from fastapi import FastAPI, HTTPException
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

EXTERNAL_SERVICE_URL = "http://localhost:8000/fake_service"

# Retry decorator: si hay 503 -> reintenta
@retry(
    stop=stop_after_attempt(3),          # reintenta 3 veces máximo
    wait=wait_fixed(2)                   # espera 2 segundos entre reintentos

    # Versión backoff exponencial
    #wait=wait_exponential(multiplier=1, min=1, max=16)

)
def call_external_service():
    response = httpx.get(EXTERNAL_SERVICE_URL)
    if response.status_code == 503:
        logger.warning(f"503 Service Unavailable, reintentando...")
        raise Exception("503 Service Unavailable")  # lanza excepción para que retry funcione
    response.raise_for_status()
    return response.json()

@app.get("/call-service/")
def call_service():
    try:
        result = call_external_service()
        return {"result": result}
    except RetryError:
        raise HTTPException(status_code=500, detail="Servicio no disponible después de varios intentos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
