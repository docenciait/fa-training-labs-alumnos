
## DOMINIO: `Pedido`

Ahora vamos a tener:

### Comandos (Commands = modifican)

1. `CrearPedido`
2. `CancelarPedido`
3. `MarcarPedidoComoEntregado`

### Consultas (Queries = solo leen)

1. `GetPedidoPorId`
2. `ListarPedidosPorUsuario`
3. `ContarPedidosPendientes`

---

##  Nuevo esquema de carpetas:

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

## 🧠 ¿Qué aprendemos con esto?

| Parte                            | Tipo    | Qué hace                      |
| -------------------------------- | ------- | ----------------------------- |
| `CancelarPedidoHandler`          | Command | Modifica estado a "cancelado" |
| `EntregarPedidoHandler`          | Command | Modifica estado a "entregado" |
| `ListarPedidosPorUsuarioHandler` | Query   | Lee múltiples pedidos         |
| `ContarPedidosPendientesHandler` | Query   | Lee solo un número            |

➡️ Cada caso tiene **su propio handler**, **su modelo específico**, y **no se mezclan roles**.

---
# Proyecto CQRS + Arquitectura Hexagonal (FastAPI + SQLite)

Este proyecto demuestra cómo aplicar **CQRS** dentro de una **arquitectura hexagonal** usando FastAPI.

## 🧱 Estructura Hexagonal + CQRS

- **Dominio**
  - `Pedido` como entidad
  - Puerto `PedidoRepositoryPort` para persistencia
- **Aplicación**
  - Casos de uso separados: `CrearPedidoHandler`, `GetPedidoHandler`
- **Infraestructura**
  - `PedidoRepositorySQLAlchemy` accede a la base de datos
- **Interfaces**
  - FastAPI como adaptador de entrada

## 📦 Endpoints

- `POST /pedidos` — crear un pedido
- `POST /pedidos/cancelar` — cancelar un pedido
- `POST /pedidos/entregar` — entregar un pedido
- `GET /pedidos/{id}` — obtener un pedido
- `GET /usuarios/{id}/pedidos` — listar pedidos por usuario
- `GET /pedidos/pendientes/count` — contar pedidos pendientes

## 🧪 Test de la API con curl

### 1. Crear un pedido

```bash
curl -X POST http://127.0.0.1:8000/pedidos \
-H "Content-Type: application/json" \
-d '{ "usuario_id": 1, "producto": "Libro", "cantidad": 2 }'
```

### 2. Obtener el pedido por ID (reemplaza `1` por el ID real retornado)

```bash
curl http://127.0.0.1:8000/pedidos/1
```

### 3. Cancelar un pedido

```bash
curl -X POST http://127.0.0.1:8000/pedidos/cancelar \
-H "Content-Type: application/json" \
-d '{ "pedido_id": 1 }'
```

### 4. Marcar un pedido como entregado

```bash
curl -X POST http://127.0.0.1:8000/pedidos/entregar \
-H "Content-Type: application/json" \
-d '{ "pedido_id": 1 }'
```

### 5. Listar pedidos de un usuario

```bash
curl http://127.0.0.1:8000/usuarios/1/pedidos
```

### 6. Contar pedidos pendientes

```bash
curl http://127.0.0.1:8000/pedidos/pendientes/count
```

## 🏁 Para ejecutar

```bash
pip install fastapi uvicorn sqlalchemy
uvicorn main:app --reload
```