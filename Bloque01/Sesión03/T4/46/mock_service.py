# mock_service.py

from fastapi import FastAPI, HTTPException
import random

app = FastAPI()

@app.get("/unstable")
def unstable_service():
    if random.random() < 0.5:  # 50% de probabilidades de fallo
        raise HTTPException(status_code=500, detail="Fallo simulado")
    return {"message": "Todo OK"}