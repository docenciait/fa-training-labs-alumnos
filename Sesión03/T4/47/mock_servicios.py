# mock_servicios.py
from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/products/{product_id}")
async def get_product_info(product_id: str):
    return {"id": product_id, "name": "Poción de Maná", "description": "Restaura 100 MP."}

@app.get("/inventory/{product_id}")
async def get_inventory(product_id: str, fail: bool = False):
    if fail:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return {"product_id": product_id, "stock": 42}