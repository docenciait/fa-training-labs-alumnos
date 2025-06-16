

# 📦 Event Sourcing aplicado en Hexagonal + CQRS

---

## 🧠 ¿Qué es Event Sourcing?

**Event Sourcing** es un patrón donde el **estado del sistema no se guarda directamente**, sino que se reconstruye **a partir de una secuencia de eventos inmutables** que han ocurrido en el tiempo.

> 👉 En lugar de guardar un `Pedido` con estado actual en una tabla, guardamos eventos como:
>
> * `PedidoCreado`
> * `PedidoConfirmado`
> * `PedidoEnviado`

---

## 🧩 Arquitectura aplicada al proyecto

```text
Solicitud HTTP POST /pedidos
          │
          ▼
  [interfaces/api/routes_pedido.py]
          │
          ▼
DTO → CrearPedidoCommand
          │
          ▼
[application/commands/crear_pedido.py]  ← ← ←  EVENT STORE
          │                               (guardar evento)
          ▼
Pedido (Entidad de dominio)
          │
          ▼
Repositorio (guardar estado actual opcional)
```

---

## 📚 Tablas y componentes explicados

### 🟦 Tabla 1: Entidades clave

| Componente                  | Tipo              | Rol                                                       |
| --------------------------- | ----------------- | --------------------------------------------------------- |
| `CrearPedidoCommandHandler` | Application       | Caso de uso que ejecuta lógica y genera eventos           |
| `PedidoCreado`              | Evento de dominio | Representa el hecho de que un pedido fue creado           |
| `EventStorePort`            | Puerto de salida  | Define interfaz para guardar y recuperar eventos          |
| `SQLiteEventStore`          | Adaptador         | Implementa la interfaz usando SQLAlchemy y SQLite         |
| `EventModel`                | Persistencia      | Representación en DB de cada evento (`event_store` tabla) |

---

### 🟦 Tabla 2: Estructura de la tabla `event_store` (SQLite)

| Columna        | Tipo        | Descripción                             |
| -------------- | ----------- | --------------------------------------- |
| `id`           | Integer     | ID autoincremental                      |
| `aggregate_id` | String      | ID del agregado (ej. ID del pedido)     |
| `event_type`   | String      | Tipo de evento (ej. "PedidoCreado")     |
| `data`         | Text (JSON) | Payload serializado del evento (`dict`) |

---

## 🧪 Ejemplo real del flujo

### 1. El usuario hace un POST:

```json
{
  "usuario_id": 1,
  "producto": "Camiseta",
  "cantidad": 3
}
```

---

### 2. Se ejecuta este flujo:

1. El endpoint recibe un `CrearPedidoDTO`
2. Se transforma a un `CrearPedidoCommand`
3. El `CrearPedidoCommandHandler`:

   * Calcula `total`
   * Crea entidad `Pedido`
   * Guarda en repositorio
   * **Emite `PedidoCreado`**
   * Llama a `SQLiteEventStore.save_event(...)`
4. Se guarda este evento:

```json
{
  "aggregate_id": "1",
  "event_type": "PedidoCreado",
  "data": {
    "id": 1,
    "usuario_id": 1,
    "producto": "Camiseta",
    "cantidad": 3,
    "total": 30.0,
    "estado": "pendiente"
  }
}
```

5. Se muestra en consola:

```bash
INFO:root:Evento emitido: PedidoCreado(id=1, usuario_id=1, ...)
```

---

## 🧱 ¿Por qué es útil Event Sourcing aquí?

| Ventaja                      | Aplicación concreta en este proyecto                      |
| ---------------------------- | --------------------------------------------------------- |
| Historial completo           | Puedes ver TODO lo que ocurrió con cada pedido            |
| Reproducibilidad             | Puedes **reconstruir** cualquier pedido desde eventos     |
| Debug y auditoría            | Cada cambio queda registrado como hecho inmutable         |
| Proyecciones independientes  | Puedes tener diferentes vistas del estado del sistema     |
| Evolución y desnormalización | Puedes derivar nuevos estados sin alterar eventos pasados |

---

## 🛠️ ¿Dónde se almacena todo?

```
event_store/
├── id = 1
├── aggregate_id = "1"
├── event_type = "PedidoCreado"
├── data = JSON con info del pedido
```

---

## 📈 ¿Qué se podría añadir después?

| Mejora            | Descripción breve                                      |
| ----------------- | ------------------------------------------------------ |
| Replay            | Reconstruir entidad desde eventos                      |
| Snapshotting      | Guardar estado actual para acelerar el replay          |
| EventBus / PubSub | Publicar eventos para que otros servicios los escuchen |
| Event versioning  | Adaptar eventos antiguos a nuevas versiones de schema  |

---
