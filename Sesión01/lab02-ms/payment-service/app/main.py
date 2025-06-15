from fastapi import FastAPI
from app.api.v1 import payments

app = FastAPI(title="Payment Service")

app.include_router(payments.router, prefix="/api/v1")