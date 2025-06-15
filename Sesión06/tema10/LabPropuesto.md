

# 🧪 LABORATORIO – Integración de WebSockets en Arquitectura Hexagonal (FastAPI, sin Redis)

### 🎯 Objetivo del laboratorio

El objetivo de este laboratorio es **integrar WebSockets como un puerto de entrada secundario** en una aplicación construida con **Arquitectura Hexagonal** y FastAPI. En lugar de utilizar una infraestructura de mensajería externa como Redis, se implementará una solución **in-memory** que gestione las conexiones activas y difunda eventos directamente desde la capa de aplicación.

---

## 🧠 Contexto

Estás desarrollando un microservicio de gestión de tareas (`TaskService`) siguiendo los principios de la arquitectura hexagonal. Hasta ahora, los casos de uso son ejecutados a través de una API REST.

Ahora, se requiere que el sistema **notifique en tiempo real a los clientes conectados por WebSocket** cuando se cree una nueva tarea.

---

## 📌 Requisitos funcionales

* Cada vez que se cree una tarea, todos los clientes conectados a través de WebSocket deben recibir una notificación en tiempo real con los datos de la tarea.
* Los clientes se conectan al endpoint WebSocket `/ws/tasks`.
* El evento se genera desde la **capa de aplicación (caso de uso)**.
* La difusión del evento se implementa mediante un **puerto de salida (EventBroadcasterPort)**.
* El canal WebSocket debe funcionar como un **adaptador de entrada (secundario)**, completamente separado del caso de uso y del dominio.

---

## 📌 Requisitos no funcionales

* No se debe utilizar Redis, Kafka ni ninguna otra infraestructura externa.
* Toda la gestión de clientes debe realizarse en memoria.
* El diseño debe respetar **Arquitectura Hexagonal**: separar dominio, aplicación, infraestructura y adaptadores de entrada.

---

## 🧱 Arquitectura esperada

```
hex_ws_tasks/
├── domain/                     # Entidades del dominio (e.g. Task)
├── application/               # Casos de uso + puertos
│   ├── usecases/
│   └── ports/
├── infrastructure/            # Adaptadores de salida (e.g. broadcaster in-memory)
├── interfaces/                # Adaptadores de entrada (REST y WebSocket)
├── main.py                    # Punto de entrada FastAPI
```

---

## ✨ Actividades que deberás completar

1. **Definir la entidad `Task`** en la capa de dominio.
2. **Definir el puerto de salida `EventBroadcasterPort`** en la capa de aplicación, que declare el método `broadcast_task_created(...)`.
3. **Implementar un adaptador de salida InMemoryBroadcaster**, que almacene conexiones WebSocket activas y difunda eventos.
4. **Implementar el caso de uso `CreateTaskUseCase`**, que reciba un `EventBroadcasterPort` y lo use para emitir el evento de tarea creada.
5. **Exponer el caso de uso mediante un endpoint REST (`POST /tasks`)**.
6. **Implementar el endpoint WebSocket `/ws/tasks`**, que registre y mantenga las conexiones WebSocket activas.
7. **Realizar pruebas manuales** usando `websocat` y `curl` para validar que los eventos se propagan correctamente.

---

## 🧪 Ejemplo de prueba manual

1. Conectarse por WebSocket:

   ```bash
   websocat ws://localhost:8000/ws/tasks
   ```

2. Crear una tarea:

   ```bash
   curl -X POST "http://localhost:8000/tasks?task_id=123&title=Hacer el lab de WebSockets"
   ```

3. Ver en la terminal del WebSocket el mensaje:

   ```
   Tarea creada: 123 - Hacer el lab de WebSockets
   ```

---
