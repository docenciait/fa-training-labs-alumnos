# test_resiliencia.py
import pytest
import respx
import httpx
from fastapi.testclient import TestClient
from main_resiliente import app # Importa tu app de FastAPI

# URLs de los servicios que vamos a mockear
PRODUCT_API_URL = "http://localhost:9001/products/mana-potion"
INVENTORY_API_URL = "http://localhost:9002/inventory/mana-potion"

client = TestClient(app)

@respx.mock
def test_endpoint_degrades_gracefully_when_inventory_fails():
    # 1. Mock del camino feliz para el servicio de productos (crítico)
    respx.get(PRODUCT_API_URL).mock(
        return_value=httpx.Response(200, json={"id": "mana-potion", "name": "Poción de Maná"})
    )
    
    # 2. Mock del CAMINO DE FALLO para el servicio de inventario (no crítico)
    respx.get(INVENTORY_API_URL).mock(
        return_value=httpx.Response(503) # Service Unavailable
    )

    # 3. Llama a nuestro endpoint
    response = client.get("/product-details/mana-potion")

    # 4. Verificaciones (Asserts)
    # El endpoint debe responder OK (200), no un error 5xx
    assert response.status_code == 200
    
    data = response.json()
    
    # La información del producto debe estar presente
    assert data["product_info"]["name"] == "Poción de Maná"
    
    # La información del inventario debe reflejar el estado de fallback
    assert data["inventory"]["stock"] is None
    assert "No se pudo verificar" in data["inventory"]["status"]

@respx.mock
def test_endpoint_fails_when_critical_service_fails():
    # Mock del servicio de productos fallando
    respx.get(PRODUCT_API_URL).mock(return_value=httpx.Response(500))
    # No necesitamos mockear el inventario porque la ejecución parará antes

    response = client.get("/product-details/mana-potion")

    # Si el servicio crítico falla, todo el endpoint debe fallar
    assert response.status_code == 502 # Bad Gateway
    assert "El servicio de productos falló" in response.json()["detail"]