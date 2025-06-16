# FastAPI Event Sourcing con Arquitectura Hexagonal

Este proyecto demuestra cómo aplicar **Event Sourcing** usando **FastAPI** y una arquitectura hexagonal, con:

- Eventos como `OrderCreated`, `OrderShipped`, `PaymentReceived`
- Un `Order` que se reconstruye desde eventos (`rebuild_order_from_events`)
- Almacenamiento de eventos con `EventStore` (interfaz) e implementación `InMemoryEventStore`
- Endpoints REST en FastAPI

## 📦 Endpoints

- `POST /orders/` — Crear pedido
- `POST /orders/{id}/ship` — Marcar como enviado
- `POST /orders/{id}/pay` — Marcar como pagado
- `GET /orders/{id}` — Obtener estado actual del pedido

## 🔁 Flujo CQRS + Event Sourcing

- Solo se guarda una secuencia de eventos.
- El estado actual se reconstruye desde ellos.
- Arquitectura hexagonal con capas bien separadas.

## 🏁 Ejecutar

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

(En esta versión inicial se usa memoria. Puedes extenderla a MariaDB y RabbitMQ como siguiente paso.)