from fastapi import FastAPI, Depends, HTTPException
from db import Base, engine, SessionLocal
from repository import PedidoRepository
from handlers.command_handler import CrearPedidoHandler, CancelarPedidoHandler, EntregarPedidoHandler
from handlers.query_handler import GetPedidoHandler, ListarPedidosPorUsuarioHandler, ContarPedidosPendientesHandler
from schemas import CreatePedidoCommand, CancelarPedidoCommand, EntregarPedidoCommand, PedidoDTO

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/pedidos", response_model=PedidoDTO)
def crear_pedido(cmd: CreatePedidoCommand, db=Depends(get_db)):
    handler = CrearPedidoHandler(PedidoRepository(db))
    pedido = handler.execute(cmd)
    return PedidoDTO.model_validate(pedido)

@app.post("/pedidos/cancelar", response_model=PedidoDTO)
def cancelar_pedido(cmd: CancelarPedidoCommand, db=Depends(get_db)):
    handler = CancelarPedidoHandler(PedidoRepository(db))
    pedido = handler.execute(cmd)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return PedidoDTO.model_validate(pedido)

@app.post("/pedidos/entregar", response_model=PedidoDTO)
def entregar_pedido(cmd: EntregarPedidoCommand, db=Depends(get_db)):
    handler = EntregarPedidoHandler(PedidoRepository(db))
    pedido = handler.execute(cmd)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return PedidoDTO.model_validate(pedido)

@app.get("/pedidos/{pedido_id}", response_model=PedidoDTO)
def obtener_pedido(pedido_id: int, db=Depends(get_db)):
    handler = GetPedidoHandler(PedidoRepository(db))
    dto = handler.execute(pedido_id)
    if not dto:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return dto

@app.get("/usuarios/{usuario_id}/pedidos", response_model=list[PedidoDTO])
def listar_pedidos(usuario_id: int, db=Depends(get_db)):
    handler = ListarPedidosPorUsuarioHandler(PedidoRepository(db))
    return handler.execute(usuario_id)

@app.get("/pedidos/pendientes/count")
def contar_pedidos_pendientes(db=Depends(get_db)):
    handler = ContarPedidosPendientesHandler(PedidoRepository(db))
    return {"pendientes": handler.execute()}