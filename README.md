# Laboratorios de Formación: De FastAPI Monolítico a Microservicios

Bienvenidos a la serie de laboratorios de formación diseñados para guiaros a través del proceso de análisis, descomposición y refactorización de una aplicación FastAPI monolítica hacia una arquitectura de microservicios moderna.

## Objetivo General

Capacitar a los desarrolladores para:
* Analizar aplicaciones monolíticas.
* Identificar y definir los límites de los microservicios.
* Implementar microservicios utilizando FastAPI.
* Aplicar patrones clave como API Gateway y Service Discovery.
* Abordar la comunicación, observabilidad y seguridad en arquitecturas de microservicios.

## Prerrequisitos

* Conocimientos básicos de Python.
* Familiaridad con los conceptos de API REST.
* Experiencia básica con FastAPI (creación de endpoints, modelos Pydantic).
* Git y GitHub básicos.
* Docker (recomendado para ejecutar los servicios).

## Estructura de los Laboratorios

Cada laboratorio se encuentra en su propia carpeta (ej. `lab01-monolith-analysis-decomposition/`) y contiene:
* Un archivo `README.md` con las instrucciones específicas del laboratorio.
* Código fuente necesario para el laboratorio.
* Plantillas o documentos de trabajo.

**Laboratorios Disponibles:**

1.  **Laboratorio 1: Análisis del Monolito y Estrategia de Descomposición**
    * Directorio: [`lab01-monolith-analysis-decomposition/`](./lab01-monolith-analysis-decomposition/)
2.  _Más laboratorios se añadirán progresivamente._

## Cómo Empezar

1.  Clona este repositorio:
    ```bash
    git clone [https://github.com/tu_usuario_o_organizacion/fastapi-microservices-training-labs.git](https://github.com/tu_usuario_o_organizacion/fastapi-microservices-training-labs.git)
    ```
2.  Navega al directorio del primer laboratorio:
    ```bash
    cd fastapi-microservices-training-labs/lab01-monolith-analysis-decomposition
    ```
3.  Sigue las instrucciones del archivo `README.md` dentro de esa carpeta.

¡Disfruta del aprendizaje!

---



# 📚 **Programa Completo de Laboratorios - 8 sesiones**

| Sesión | Laboratorio                                                                                         | Objetivos                                                                                                             | Temas Cubiertos                                                                        | Producto Final                                                     |
| :----: | :-------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- | :----------------------------------------------------------------- |
|    1   | **Lab 1: Monolito → Microservicios + API Gateway + Seguridad Básica**                               | Migrar un monolito a microservicios, montar API Gateway (NGINX) y primera seguridad (HTTPS + CORS + JWT básico)       | Arquitectura básica, API Gateway, HTTPS, CORS, Autenticación JWT                       | Microservicio `Users` + API Gateway protegido                      |
|    2   | **Lab 2: Configuración Profesional + Gestión de Rutas + Dependencias**                              | Configuración por entorno, DI con FastAPI, Validación Inputs/Outputs, Middlewares, Excepciones Personalizadas         | BaseSettings, Dependency Injection, Validación Pydantic, Middlewares, Manejo Errores   | Microservicio Users completo, configurado para diferentes entornos |
|    3   | **Lab 3: Comunicación REST entre Microservicios + Seguridad OAuth2 + Rate Limiting**                | Comunicación Users-Orders, OAuth2 Auth Server propio, Rate Limiting, Políticas de CORS estrictas                      | Comunicación RESTful, OAuth2, Rate Limiting, CORS Estricto                             | Auth Server + Services seguros comunicándose                       |
|    4   | **Lab 4: Arquitectura Hexagonal + DDD + CQRS + Testing Unitario**                                   | Implementar Arquitectura Hexagonal, aplicar DDD básico, separar Commands/Queries (CQRS), tests unitarios con Pytest   | Hexagonal, Ports & Adapters, DDD táctico, CQRS Commands/Queries, Pytest Unitario       | Microservicio Hexagonal `Users` con tests unitarios                |
|    5   | **Lab 5: Persistencia Avanzada + Event Sourcing + RabbitMQ**                                        | Persistencia SQL (SQLAlchemy) + MongoDB, Eventos de Dominio + Event Sourcing + Integración RabbitMQ                   | SQLAlchemy ORM, MongoDB Motor, Event Sourcing, Domain Events, RabbitMQ Async Messaging | Persistencia distribuida + Microservicios event-driven             |
|    6   | **Lab 6: Kafka + WebSockets + Notificaciones Tiempo Real + Seguridad WS**                           | Integración Kafka, Servidor WebSocket Seguro (JWT en WS), Microservicio Notificaciones                                | Kafka, aiokafka, WebSocket FastAPI, JWT WS, Redis PubSub opcional                      | Sistema de Notificaciones Realtime seguro                          |
|    7   | **Lab 7: Escalabilidad: Redis Caching + Profiling + Docker Compose Avanzado + Testing Integración** | Caching Redis, Profiling Performance, Redes Docker Compose + Testing Integración + Coverage                           | Redis, Profiling, Docker Compose Redes, Pytest Integration, Coverage Reports           | Sistema escalable, cacheado y testeado                             |
|    8   | **Lab 8: Observabilidad (Prometheus/Grafana/Loki) + CI/CD Pipelines + Proyecto Final**              | Integrar Observabilidad completa (Prometheus, Grafana, Loki), Dockerfiles productivos, GitHub Actions CI/CD Pipelines | Observabilidad, Metrics/Logs Centralizados, GitHub Actions CI/CD, Helm/Kustomize       | Sistema empresarial productivo con observabilidad y CI/CD          |

---

# 🛠️ **Detalle Completo por Sesión**

---

### 1️⃣ **Sesión 1 — Lab 1: Monolito → Microservicios + API Gateway + Seguridad Básica**

* **Objetivos**:

  * Migrar aplicación monolítica inicial a microservicios `Users`.
  * Configurar un API Gateway con **NGINX** (HTTPS, Reverse Proxy).
  * Configurar **CORS**, **Validación de Inputs/Outputs**.
  * Autenticación inicial con **JWT Tokens** (Bearer Authentication).
* **Tecnologías**:

  * FastAPI, Docker Compose, NGINX, OpenSSL (auto-signed certs), HTTPS, PyJWT.
* **Producto Final**:

  * Primer Microservicio `Users` detrás de un API Gateway HTTPS con CORS seguro y JWT básico.

---

### 2️⃣ **Sesión 2 — Lab 2: Configuración Profesional + Rutas Limpias + Dependency Injection**

* **Objetivos**:

  * Separación en carpetas limpia: `routers`, `services`, `schemas`.
  * `BaseSettings` para configuración profesional por entorno (dev, staging, prod).
  * Inyección de dependencias (`Depends`), middlewares personalizados (log de Request/Response).
  * Excepciones personalizadas y validaciones profundas.
* **Tecnologías**:

  * FastAPI, Pydantic BaseSettings, Middlewares, Custom Exceptions.
* **Producto Final**:

  * Microservicio `Users` limpio, desacoplado, dependencias inyectadas, configuración por entorno.

---

### 3️⃣ **Sesión 3 — Lab 3: Comunicación REST entre Microservicios + Auth Server OAuth2 + Rate Limiting**

* **Objetivos**:

  * Crear microservicios `Users`, `Orders`, `Payments`.
  * Implementar servidor de autenticación OAuth2 propio.
  * Protección de endpoints REST con OAuth2 (password flow).
  * Rate Limiting por IP con FastAPI Limiter.
* **Tecnologías**:

  * FastAPI OAuth2 Password, Rate Limiter, Docker Compose, OAuth2 Scopes.
* **Producto Final**:

  * 3 Microservicios comunicándose via REST + Seguridad OAuth2 + Rate Limit por IP.

---

### 4️⃣ **Sesión 4 — Lab 4: Hexagonal + DDD + CQRS + Testing Unitario**

* **Objetivos**:

  * Implementar Patrón Hexagonal completo (Domain, Application, Infrastructure).
  * Aplicar tácticas DDD (Entities, Aggregates, Value Objects).
  * Aplicar CQRS puro: separación Commands / Queries.
  * Testing Unitario exhaustivo de capas de dominio.
* **Tecnologías**:

  * FastAPI, Arquitectura Hexagonal, Pydantic, Pytest Unitario.
* **Producto Final**:

  * Microservicio Users hexagonal 100% testeado, separación CQRS.

---

### 5️⃣ **Sesión 5 — Lab 5: Persistencia Avanzada + Event Sourcing + RabbitMQ**

* **Objetivos**:

  * Persistencia en **MariaDB** (SQLAlchemy ORM) y **MongoDB** (Motor Async).
  * Patrones de Repositorio desacoplado.
  * Implementar **Eventos de Dominio** y **Event Sourcing**.
  * Integración RabbitMQ para Pub/Sub Eventual Consistency.
* **Tecnologías**:

  * SQLAlchemy, MongoDB (Motor), Alembic, RabbitMQ, Events Pattern.
* **Producto Final**:

  * Microservicio Users/Orders persistiendo en BDDs + Event Sourcing + Eventos de Dominio.

---

### 6️⃣ **Sesión 6 — Lab 6: Kafka + WebSocket + Notificaciones + Seguridad WS**

* **Objetivos**:

  * Integración Kafka: productor/consumidor.
  * Servidor WebSocket para notificaciones en tiempo real.
  * Seguridad WebSocket con autenticación JWT por conexión.
  * Opcional Redis para Pub/Sub.
* **Tecnologías**:

  * aiokafka, FastAPI WebSocket, JWT Auth para WS, Redis.
* **Producto Final**:

  * Microservicio de notificaciones real-time seguro vía WebSocket/Kafka.

---

### 7️⃣ **Sesión 7 — Lab 7: Escalabilidad + Redis Cache + Profiling + Testing Integración**

* **Objetivos**:

  * Introducir Caching con Redis para endpoints críticos.
  * Balanceo de carga básico con Docker Compose (NGINX como LB).
  * Profiling de servicios: detectar bottlenecks (cProfile, PyInstrument).
  * Testing de Integración entre Microservicios (Pytest + Coverage).
* **Tecnologías**:

  * Redis, Docker Compose Redes, Pytest Integration, Coverage, Profiling.
* **Producto Final**:

  * Sistema cacheado, balanceado y probado E2E entre servicios.

---

### 8️⃣ **Sesión 8 — Lab 8: Observabilidad Completa + CI/CD + Proyecto Final**

* **Objetivos**:

  * Configurar métricas y logs centralizados: Prometheus + Grafana + Loki.
  * Dockerfiles optimizados multistage + docker-compose.prod.yml.
  * CI/CD Pipelines GitHub Actions: Build, Test, Deploy.
  * Deploy en Kubernetes opcional (Helm/Kustomize).
* **Tecnologías**:

  * Prometheus, Grafana, Loki, Docker Multistage, GitHub Actions, Kubernetes Helm.
* **Producto Final**:

  * Proyecto final de microservicios productivo: Observabilidad + Pipelines CI/CD completos.

---

# ✅ **Cobertura Completa Temario VS Laboratorios**

| Tema                            | ¿Incluido en Laboratorio? | Comentarios                                |
| :------------------------------ | :------------------------ | :----------------------------------------- |
| Arquitectura Microservicios     | ✅                         | Desde Sesión 1                             |
| FastAPI Framework               | ✅                         | Base de todos los labs                     |
| Comunicación Síncrona/Asíncrona | ✅                         | REST, RabbitMQ, Kafka                      |
| Manejo Errores, Circuit Breaker | ✅                         | Errores personalizados, pybreaker opcional |
| Seguridad JWT/OAuth2            | ✅                         | JWT Session 1 y OAuth2 Session 3           |
| Arquitectura Hexagonal          | ✅                         | Sesión 4                                   |
| DDD, CQRS, Event Sourcing       | ✅                         | Sesión 4 y 5                               |
| Kafka y RabbitMQ                | ✅                         | Sesión 5 y 6                               |
| WebSockets + Pub/Sub            | ✅                         | Sesión 6                                   |
| Diseño APIs REST y WS           | ✅                         | Desde Session 1, 3, 6                      |
| Escalabilidad, Redis, Caching   | ✅                         | Sesión 7                                   |
| Persistencia de Datos           | ✅                         | MariaDB, MongoDB, SQLAlchemy               |
| Testing Pytest                  | ✅                         | Sesión 4, 7                                |
| Observabilidad                  | ✅                         | Prometheus, Grafana, Loki Sesión 8         |
| CI/CD Pipelines                 | ✅                         | GitHub Actions Sesión 8                    |
| Kubernetes Deployment           | ✅                         | Opcional en Sesión 8                       |

---

# 🚀 **Resultado Final al terminar**

* Microservicios diseñados profesionalmente (Hexagonal + DDD + CQRS).
* APIs seguras (OAuth2, JWT, HTTPS, CORS, Rate Limiting).
* Comunicación mixta REST + RabbitMQ + Kafka.
* Persistencia distribuida SQL + NoSQL.
* Event Sourcing y Eventos de Dominio.
* WebSockets en Tiempo Real protegidos.
* Pruebas Unitarias e Integración + Coverage.
* Observabilidad: Prometheus, Grafana, Loki.
* CI/CD Pipelines GitHub Actions con despliegues automáticos.

---

# 🎯 **¿Quieres ahora que te entregue:**

* Un **Plan de Sesión** detallado (por hora)?
* Un **Set de repositorios iniciales** para cada lab?
* Una **Guía para instructores** con ejemplos de solución (repos finales)?
* ¿O directamente el ZIP base de todos los Labs (Init + Final)?

👉 **Dime si quieres esto más en formato *Markdown* o *Excel* bien maquetado para empresa.**
