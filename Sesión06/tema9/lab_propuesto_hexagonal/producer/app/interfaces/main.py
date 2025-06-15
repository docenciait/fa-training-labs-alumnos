from fastapi import FastAPI
from app.interfaces.api.routes import router

app = FastAPI()
app.include_router(router)