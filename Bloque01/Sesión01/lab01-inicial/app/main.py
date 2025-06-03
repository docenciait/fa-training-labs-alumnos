from fastapi import FastAPI
from app.api.v1 import users, products, orders, payments
from app.db.database import Base, engine

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Monolito 2025 🚀")

# Routers
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
