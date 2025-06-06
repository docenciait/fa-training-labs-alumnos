from fastapi import FastAPI
from app.api.v1 import users

app = FastAPI(title="Auth Service")

app.include_router(users.router, prefix="/api/v1")
