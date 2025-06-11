from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import asyncio

from app.interfaces.api.product_routes import router
from app.infrastructure.db_models.product_model import Base
from app.infrastructure.database import engine

app = FastAPI(title="Product Microservice - Hexagonal")
app.include_router(router)

@app.on_event("startup")
async def startup():
    retries = 10
    delay = 3
    for i in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Base de datos conectada y tablas creadas.")
            break
        except OperationalError as e:
            print(f"🔁 Esperando conexión a la base de datos... (intento {i+1}/{retries})")
            await asyncio.sleep(delay)
    else:
        print("❌ No se pudo conectar a la base de datos.")
        raise

@app.get("/health")
async def health():
    return {"status": "ok"}
