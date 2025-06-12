from fastapi import FastAPI
from app.interfaces.api.routes import router
import asyncio
from app.infrastructure.rabbit.consumer import consume

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())