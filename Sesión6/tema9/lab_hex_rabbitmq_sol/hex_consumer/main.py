from fastapi import FastAPI
from app.interfaces.api.routes import router
from app.infrastructure.rabbit.consumer import setup_consumer

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    setup_consumer()
