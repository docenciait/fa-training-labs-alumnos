from dataclasses import dataclass

@dataclass
class Pedido:
    id: int | None
    usuario_id: int
    producto: str
    cantidad: int
    total: float
    estado: str
