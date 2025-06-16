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
- `GET /pedidos/{id}` — obtener un pedido

## 🏁 Para ejecutar

```bash
pip install fastapi uvicorn sqlalchemy
uvicorn main:app --reload
```

## ✅ Ventajas

- Separación clara entre lectura y escritura (CQRS)
- Arquitectura mantenible y escalable
- Dominio independiente de infraestructura