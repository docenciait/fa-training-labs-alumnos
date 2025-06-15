# mock_service.py

from fastapi import FastAPI, HTTPException
import random

app = FastAPI()

# No vamos a poner aletoriedad porque no se prueba bien
# Simplemente cuando queramos que falle, cancelamos el servicio y cuando queramos
# que funcione lo levantamos

@app.get("/unstable")
def unstable_service():
    # if random.random() < 0.5:  # 50% de probabilidades de fallo
    #     raise HTTPException(status_code=500, detail="Fallo simulado")
    return {"message": "Todo OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)