## main.py

from fastapi import FastAPI, HTTPException
import httpx
import pybreaker
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Listener para ver el estado del breaker
class MyListener(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        logger.warning(f"Circuit Breaker {cb.name} cambió de {old_state.name} a {new_state.name}")

# Circuit Breaker configuración
breaker = pybreaker.CircuitBreaker(
    fail_max=3,            # Máximo 3 fallos para abrir
    reset_timeout=10,      # 10 segundos antes de HALF-OPEN
    listeners=[MyListener()],
    name="MockServiceBreaker"
)

app = FastAPI()

URL = "http://localhost:8000/unstable"  # Nuestro servicio inestable

# Función protegida
@breaker
def call_mock_service():
    response = httpx.get(URL, timeout=2.0)
    response.raise_for_status()  # Lanza excepción en error HTTP
    return response.json()

# Endpoint para probar
@app.get("/call-external")
def get_mock_service():
    try:
        data = call_mock_service()
        return {"status": "ok", "data": data}
    except pybreaker.CircuitBreakerError:
        logger.error("Circuit Breaker ABIERTO. Servicio Mock NO disponible.")
        raise HTTPException(status_code=503, detail="Servicio no disponible (Circuito Abierto).")
    except Exception as e:
        logger.error(f"Error contactando servicio Mock: {e}")
        raise HTTPException(status_code=502, detail="Error contactando servicio externo.")

# Endpoint para ver el estado del breaker
@app.get("/breaker-status")
def breaker_status():
    return {
        "state": breaker.current_state,  # <-- CORRECTED LINE
        "failures": breaker.fail_counter
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)