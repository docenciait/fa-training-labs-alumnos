class Pedido:
    def __init__(self, usuario_id: int, producto: str, cantidad: int):
        self.usuario_id = usuario_id
        self.producto = producto
        self.cantidad = cantidad
        self.total = cantidad * 10
        self.estado = "pendiente"