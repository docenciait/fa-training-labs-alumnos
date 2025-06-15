from fastapi import FastAPI
from app.interfaces.api import router

app = FastAPI(title="Productor")
app.include_router(router)