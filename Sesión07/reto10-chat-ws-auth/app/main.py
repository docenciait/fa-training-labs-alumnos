
from fastapi import FastAPI
from app.interfaces.auth_http import router as auth_router
from app.interfaces.ws_chat import router as ws_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(ws_router)
