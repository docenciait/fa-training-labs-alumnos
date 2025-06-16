from fastapi import FastAPI, Depends, HTTPException
from db import Base, engine, SessionLocal
from repository import PedidoRepository
from handlers.command_handler import CrearPedidoHandler
from handlers.query_handler import GetPedidoHandler
from schemas import CreatePedidoCommand, PedidoDTO
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/pedidos", response_model=PedidoDTO)
def crear_pedido(command: CreatePedidoCommand, db=Depends(get_db)):
    handler = CrearPedidoHandler(PedidoRepository(db))
    pedido = handler.execute(command)
    return PedidoDTO.model_validate(pedido)


@app.get("/pedidos/{pedido_id}", response_model=PedidoDTO)
def obtener_pedido(pedido_id: int, db=Depends(get_db)):
    handler = GetPedidoHandler(PedidoRepository(db))
    dto = handler.execute(pedido_id)
    if dto is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return dto

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)