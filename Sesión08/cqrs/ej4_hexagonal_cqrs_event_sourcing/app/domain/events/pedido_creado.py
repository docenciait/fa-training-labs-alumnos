from dataclasses import dataclass

@dataclass
class PedidoCreado:
    id: int
    usuario_id: int
    producto: str
    cantidad: int
    total: float
    estado: str
