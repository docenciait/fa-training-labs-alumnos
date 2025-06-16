from fastapi import FastAPI
from app.interfaces.http.api import router

app = FastAPI()
app.include_router(router)