# CASO: 

Vamos a **ampliar este ejemplo CQRS** con **más comandos y más queries** sobre el dominio `Pedido`, para que veas **cómo se sigue aplicando el patrón CQRS** en cada caso.


## DOMINIO: `Pedido`

Ahora vamos a tener:

### ✳ Comandos (Commands = modifican)

1. `CrearPedido`
2. `CancelarPedido`
3. `MarcarPedidoComoEntregado`

### 🔎 Consultas (Queries = solo leen)

1. `GetPedidoPorId`
2. `ListarPedidosPorUsuario`
3. `ContarPedidosPendientes`

---

## 📁 Nuevo esquema de carpetas:

```
.
├── main.py
├── db.py
├── models.py
├── schemas.py
├── repository.py
└── handlers/
    ├── command_handler.py
    └── query_handler.py
```

---

## 🟨 NUEVOS COMANDOS en `schemas.py`

```python
from pydantic import BaseModel

class CrearPedidoCommand(BaseModel):
    usuario_id: int
    producto: str
    cantidad: int

class CancelarPedidoCommand(BaseModel):
    pedido_id: int

class EntregarPedidoCommand(BaseModel):
    pedido_id: int
```

---

## 🟦 NUEVAS QUERIES en `schemas.py`

```python
class PedidoDTO(BaseModel):
    id: int
    usuario_id: int
    producto: str
    cantidad: int
    total: float
    estado: str  # nuevo campo

    model_config = {"from_attributes": True}
```

---

## 🧱 NUEVOS CAMPOS en `models.py`

```python
from sqlalchemy import Column, Integer, String, Float
from db import Base

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)
    producto = Column(String)
    cantidad = Column(Integer)
    total = Column(Float)
    estado = Column(String, default="pendiente")  # nuevo campo
```

---

## 🔧 `command_handler.py` (handlers nuevos)

```python
class CancelarPedidoHandler:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, command):
        pedido = self.repo.get_by_id(command.pedido_id)
        if pedido:
            pedido.estado = "cancelado"
            self.repo.save(pedido)
        return pedido

class EntregarPedidoHandler:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, command):
        pedido = self.repo.get_by_id(command.pedido_id)
        if pedido:
            pedido.estado = "entregado"
            self.repo.save(pedido)
        return pedido
```

---

## 🔎 `query_handler.py` (handlers nuevos)

```python
class ListarPedidosPorUsuarioHandler:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, usuario_id: int):
        pedidos = self.repo.get_all_by_usuario(usuario_id)
        return [PedidoDTO.from_orm(p) for p in pedidos]

class ContarPedidosPendientesHandler:
    def __init__(self, repo):
        self.repo = repo

    def execute(self):
        return self.repo.count_by_estado("pendiente")
```

---

## 🗃 Métodos nuevos en `repository.py`

```python
def get_all_by_usuario(self, usuario_id: int):
    return self.db.query(Pedido).filter_by(usuario_id=usuario_id).all()

def count_by_estado(self, estado: str):
    return self.db.query(Pedido).filter_by(estado=estado).count()
```

---

## 🚀 Nuevos endpoints en `main.py`

```python
@app.post("/pedidos/cancelar")
def cancelar_pedido(cmd: CancelarPedidoCommand, db=Depends(get_db)):
    handler = CancelarPedidoHandler(PedidoRepository(db))
    return handler.execute(cmd)

@app.post("/pedidos/entregar")
def entregar_pedido(cmd: EntregarPedidoCommand, db=Depends(get_db)):
    handler = EntregarPedidoHandler(PedidoRepository(db))
    return handler.execute(cmd)

@app.get("/usuarios/{usuario_id}/pedidos", response_model=list[PedidoDTO])
def listar_pedidos(usuario_id: int, db=Depends(get_db)):
    handler = ListarPedidosPorUsuarioHandler(PedidoRepository(db))
    return handler.execute(usuario_id)

@app.get("/pedidos/pendientes/count")
def contar_pendientes(db=Depends(get_db)):
    handler = ContarPedidosPendientesHandler(PedidoRepository(db))
    return {"pendientes": handler.execute()}
```

---

## ¿Qué aprendemos con esto?

| Parte                            | Tipo    | Qué hace                      |
| -------------------------------- | ------- | ----------------------------- |
| `CancelarPedidoHandler`          | Command | Modifica estado a "cancelado" |
| `EntregarPedidoHandler`          | Command | Modifica estado a "entregado" |
| `ListarPedidosPorUsuarioHandler` | Query   | Lee múltiples pedidos         |
| `ContarPedidosPendientesHandler` | Query   | Lee solo un número            |

➡️ Cada caso tiene **su propio handler**, **su modelo específico**, y **no se mezclan roles**.

