from pydantic import BaseModel

class CrearPedidoCommand(BaseModel):
    usuario_id: int
    producto: str
    cantidad: int

# Comandos nuevos
# Nuevo para CMD
class CancelarPedidoCommand(BaseModel):
    pedido_id: int

# Igualmente nuevo CMD 
class EntregarPedidoCommand(BaseModel):
    pedido_id: int

class PedidoDTO(BaseModel):
    id: int
    usuario_id: int
    producto: str
    cantidad: int
    total: float
    # Nuevo campo para Query
    estado: str

    model_config = {"from_attributes": True}