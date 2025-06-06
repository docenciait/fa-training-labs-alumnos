from fastapi import FastAPI
from app.api.v1 import orders

app = FastAPI(title="Order Service")

app.include_router(orders.router, prefix="/api/v1")