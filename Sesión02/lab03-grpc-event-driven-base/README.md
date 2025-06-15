
# 🚀  LAB 03 – gRPC + RabbitMQ (Pub/Sub)

---

# 📚 **1. ¿Qué vamos a hacer en gRPC primero?**

✅ **Primera parte: gRPC** — **Síncrono**
(Comunicación directa **Service-to-Service**, bajo contrato definido con `.proto`)

* **Objetivo**: `order-service` necesita consultar a `user-service` para saber si un `user_id` existe.
* **Tecnología**: gRPC, Protocol Buffers.
* **Qué haremos**:

  * Crear `.proto` file.
  * Montar `user-service` como **servidor** gRPC.
  * Montar `order-service` como **cliente** gRPC.

---

# 📚 **2. ¿Qué vamos a hacer después con RabbitMQ?**

✅ **Segunda parte: RabbitMQ (Pub/Sub)** — **Asíncrono**

* **Objetivo**: Cuando `order-service` cree un pedido, publicará un **evento** `order_created` en RabbitMQ.
* **Nuevo servicio**: `notification-service`, que escuchará los eventos `order_created`.
* **Tecnología**: RabbitMQ, Event-Driven Architecture.
* **Qué haremos**:

  * Añadir **RabbitMQ** a `docker-compose.yml`.
  * `order-service` será **publisher** en RabbitMQ.
  * Crear `notification-service` que será **subscriber**.
  * Simular que `notification-service` manda un email/log al recibir un evento.

---

# 📚 **3. ¿Dónde va cada cosa?**

|       Componente       |           Tipo           |                    ¿Dónde va?                   |
| :--------------------: | :----------------------: | :---------------------------------------------: |
| `.proto` + gRPC server |     **user-service**     |          Define la API gRPC y responde.         |
|       gRPC client      |     **order-service**    |         Consulta gRPC a `user-service`.         |
|     RabbitMQ Broker    |  **docker-compose.yml**  |            Nuevo servicio `rabbitmq`.           |
|    Publisher eventos   |     **order-service**    |             Publica `order_created`.            |
|   Subscriber eventos   | **notification-service** | Escucha eventos y simula enviar notificaciones. |

---

# 🛠️ **4. Actualización `docker-compose.yml`**

💡 Antes de seguir, **RabbitMQ** tiene que estar en `docker-compose.yml` para poder usar Pub/Sub.

Así que, en el mismo `docker-compose.yml`, añadimos:

```yaml
rabbitmq:
  image: rabbitmq:3-management
  container_name: rabbitmq
  ports:
    - "5672:5672"    # RabbitMQ protocol port
    - "15672:15672"  # RabbitMQ management UI
  networks:
    - lab03_net
```

✅ **Con esto:**

* `5672` es el puerto que usarán los microservicios para hablar con RabbitMQ.
* `15672` es un dashboard web para que puedas ver las colas en tu navegador ([http://localhost:15672](http://localhost:15672)).

---

# 📝 **Resumen:**

|          Paso         |                        Qué haremos                        |
| :-------------------: | :-------------------------------------------------------: |
|   Actualizar Compose  |                 Añadir `rabbitmq` broker.                 |
|    `.proto` de gRPC   |            Definir contratos de `user-service`.           |
|     Servidor gRPC     |               Implementar en `user-service`.              |
|      Cliente gRPC     |              Implementar en `order-service`.              |
| Publisher en RabbitMQ |      `order-service` publica evento `order_created`.      |
|       Subscriber      | `notification-service` escucha `order_created` y procesa. |

---

