# main_resiliente.py
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

PRODUCT_API_URL = "http://localhost:9001/products"
INVENTORY_API_URL = "http://localhost:9002/inventory"

@app.get("/product-details/{product_id}")
async def get_product_details(product_id: str):
    try:
        async with httpx.AsyncClient() as client:
            # 1. Obtener información principal (crítica)
            product_response = await client.get(f"{PRODUCT_API_URL}/{product_id}")
            product_response.raise_for_status() # Si esto falla, el endpoint entero falla
            product_data = product_response.json()

            # 2. Obtener stock (no crítico) con fallback
            stock_data = {"stock": None, "status": "No se pudo verificar el stock"}
            try:
                inventory_response = await client.get(f"{INVENTORY_API_URL}/{product_id}", timeout=2.0)
                inventory_response.raise_for_status()
                stock_data = {"stock": inventory_response.json()["stock"], "status": "Verificado"}
            except (httpx.RequestError, httpx.HTTPStatusError):
                # Fallback: Si la llamada al inventario falla, no rompemos.
                # Simplemente usamos los datos por defecto y seguimos.
                pass

            # 3. Componer la respuesta final
            return {
                "product_info": product_data,
                "inventory": stock_data
            }

    except httpx.HTTPStatusError as e:
        # Si el servicio crítico de productos falla
        raise HTTPException(status_code=502, detail=f"El servicio de productos falló: {e.response.status_code}")