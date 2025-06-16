from dataclasses import dataclass

@dataclass
class CrearPedidoCommand:
    usuario_id: int
    producto: str
    cantidad: int
