from fastapi import FastAPI
from app.api.v1 import products

app = FastAPI(title="Product Service")

app.include_router(products.router, prefix="/api/v1")