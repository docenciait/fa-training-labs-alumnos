# fake_service.py
from fastapi import FastAPI, Response
import random

app = FastAPI()

@app.get("/fake_service")
def fake_service():
    if random.random() < 0.3:
        return Response(content="{'error': 'Temporary failure'}", status_code=503, media_type="application/json")
    return {"message": "Service OK"}
