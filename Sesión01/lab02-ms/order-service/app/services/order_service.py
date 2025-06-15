from app.db import crud_order
from app.schemas.order import OrderCreate
import httpx

async def verify_user(user_id: int) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://auth-service:8000/api/v1/users/{user_id}")
        return response.status_code == 200

async def verify_products(product_ids: list) -> bool:
    async with httpx.AsyncClient() as client:
        for pid in product_ids:
            response = await client.get(f"http://product-service:8000/api/v1/products/{pid}")
            if response.status_code != 200:
                return False
    return True

async def create_order(order: OrderCreate):
    if not await verify_user(order.user_id):
        raise ValueError("User does not exist.")

    if not await verify_products(order.product_ids):
        raise ValueError("One or more products do not exist.")

    return crud_order.create_order(order)


def get_order_by_id(order_id: int):
    return crud_order.get_order_by_id(order_id)


def get_all_orders():
    return crud_order.get_all_orders()