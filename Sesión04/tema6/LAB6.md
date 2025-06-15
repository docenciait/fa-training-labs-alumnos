

# 🔹 LAB 6 – Aplicación Hexagonal con FastAPI

| Ítem                | Detalles                                                                                                                                                                                                  |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🕒 **Duración**     | 2 h (puede extenderse a 2.5h con testing)                                                                                                                                                                 |
| 🎯 **Objetivo**     | Aplicar los principios de arquitectura hexagonal para diseñar una API limpia, mantenible y desacoplada                                                                                                    |
| 🧠 **Temas**        | Tema 6 completo: Arquitectura Hexagonal, Puertos y Adaptadores, DDD básico                                                                                                                                |
| ⚙️ **Tecnologías**  | FastAPI, Pydantic, pytest, Python 3.12, Docker                                                                                                                                                            |
| 📁 **Entregable**   | Aplicación funcional estructurada en capas hexagonales, con puertos bien definidos y adaptadores de entrada y salida                                                                                      |
| 🧪 **Tareas clave** | <ul><li>Definir dominio y casos de uso</li><li>Separar puertos y adaptadores</li><li>Implementar REST como adaptador de entrada</li><li>Simular un repositorio externo como adaptador de salida</li></ul> |
| 🧩 **Repositorio**  | `lab06-hexagonal-fastapi`                                                                                                                                                                                 |

---

## ✅ Enunciado del Laboratorio

### 🧩 Contexto

Estás desarrollando una API de gestión de tareas (Task Management API) como parte de una arquitectura moderna basada en microservicios. El objetivo de este laboratorio es diseñar dicha API aplicando **arquitectura hexagonal** (también conocida como "puertos y adaptadores").

Queremos que la lógica de negocio (dominio) esté completamente desacoplada de cualquier tecnología externa (HTTP, DB, etc.), de forma que pueda ser fácilmente testeada, reutilizada y mantenida.

---

## 🎯 Objetivo Final

Crear una aplicación FastAPI con arquitectura hexagonal que:

* Exponga una API REST con endpoints para crear, consultar y actualizar tareas.
* Separe la lógica de dominio de la infraestructura.
* Defina interfaces (puertos) para los adaptadores entrantes (REST) y salientes (repositorio).
* Permita sustituir el repositorio en memoria por otro persistente sin afectar al dominio.

---

## 🗂️ Requisitos Funcionales

* El sistema gestiona **tareas**, que contienen:

  * `id` (UUID)
  * `title` (str)
  * `description` (str)
  * `completed` (bool)
* Debe permitir:

  * Crear una nueva tarea
  * Obtener todas las tareas
  * Marcar una tarea como completada

---

## 🧩 Requisitos de Arquitectura

Debes estructurar tu proyecto en las siguientes capas:

```
project/
│
├── app/
│   ├── domain/                 # Núcleo de dominio
│   │   ├── models.py           # Entidades (Tarea)
│   │   ├── ports.py            # Puertos de entrada/salida
│   │   └── services.py         # Casos de uso
│   │
│   ├── infrastructure/         # Adaptadores de salida (repositorios, almacenamiento)
│   │   └── in_memory_repo.py   # Repositorio en memoria
│   │
│   ├── interfaces/             # Adaptadores de entrada (FastAPI HTTP)
│   │   └── routes.py
│   │
│   └── main.py                 # Arranque de la app
│
├── tests/
│   ├── test_services.py        # Pruebas de lógica de dominio
│   └── test_routes.py          # Pruebas de la API HTTP
│
├── requirements.txt
└── README.md
```

---

## 🔧 Instrucciones

### 1. Crea las entidades del dominio

Define una clase `Task` como entidad de dominio. Usa tipos estándar, sin depender de Pydantic ni FastAPI.

```python
# app/domain/models.py
class Task:
    def __init__(self, id: UUID, title: str, description: str, completed: bool = False):
        ...
```

---

### 2. Define puertos

Crea interfaces para:

* El puerto de salida `TaskRepository` (guardar, obtener, actualizar tareas).
* El puerto de entrada `TaskService` (crear tarea, marcar como completada, listar).

---

### 3. Implementa casos de uso en `services.py`

La clase `TaskService` debe usar el `TaskRepository` (puerto) como dependencia.

---

### 4. Crea adaptador de salida: `InMemoryTaskRepository`

Este adaptador implementa `TaskRepository` con una simple lista en memoria. No uses ninguna base de datos externa.

---

### 5. Crea adaptador de entrada HTTP (FastAPI)

Define endpoints en `/tasks` que:

* POST `/tasks/`: crear nueva tarea
* GET `/tasks/`: listar tareas
* PATCH `/tasks/{id}/complete`: marcar tarea como completada

Este adaptador debe convertir las peticiones HTTP en llamadas a los servicios de dominio.

---

### 6. Inyecta dependencias en `main.py`

Crea la instancia del servicio y pasa el repositorio inyectado.

---

## 🧪 Bonus: Testing

* Añade tests unitarios para `TaskService`.
* Añade tests de integración para la API.

---

## 🧠 Preguntas de reflexión

1. ¿Qué ventajas aporta separar puertos y adaptadores?
2. ¿Cómo podrías reemplazar el repositorio en memoria por una base de datos sin tocar la lógica del dominio?
3. ¿Qué otros tipos de adaptadores de entrada podrías añadir además de REST?
4. ¿Qué ocurriría si implementaras eventos de dominio en esta arquitectura?

---

## 🚀 Entregable

Repositorio `lab06-hexagonal-fastapi` con:

* Código organizado en capas hexagonales.
* Adaptadores correctamente implementados.
* API REST funcional y testeada.
* README explicativo.

---

¿Quieres que prepare el repositorio inicial con esta estructura vacía y un README con el enunciado? ¿O pasamos antes a diseñar la **guía del profesor**?
