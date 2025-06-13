## 1. Levantamos los servicios

```bash
docker compose up -d --build
```


![alt text](image.png)


## 2. Vemos cómo se ha recibido el ack del consumidor

- Prueba:

```bash
curl -X 'POST' \
  'http://localhost:8000/send' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tipo": "msg",
  "id": "Identificador 1",
  "payload": {
    "additionalProp1": {"name":"John"}
  }
}'
```

![alt text](image-4.png)

## Otro ejemplo seguido

![alt text](image-5.png)


Tu ejemplo implementa una **arquitectura request/response sobre RabbitMQ** con FastAPI, usando **mensajes con `reply_to` y `correlation_id`**, lo cual es perfecto para lograr confirmaciones tipo ACK entre productor y consumidor.

Te lo explico **paso a paso con perspectiva de arquitectura hexagonal** y **flujo de eventos**, para que quede claro.

---

## 🧱 Arquitectura Productor–Consumidor con ACK (Request–Response)

```
╔══════════════╗        ╔══════════════╗        ╔══════════════╗
║ Productor    ║ ─────▶ ║ RabbitMQ     ║ ─────▶ ║ Consumidor   ║
║ FastAPI POST ║        ║ Queue: msgs  ║        ║ FastAPI      ║
║ /send        ║ ◀───── ║ Queue: temp  ║ ◀───── ║ Procesa evento y responde
╚══════════════╝        ╚══════════════╝        ╚══════════════╝
```

---

## ⚙️ Detalles Técnicos de la Implementación

### 🔵 Productor (`/send`)

1. **Crea conexión a RabbitMQ** y canal.
2. **Declara la cola principal `mensajes`** (donde escucha el consumidor).
3. **Declara una cola anónima temporal (`exclusive=True`)** que servirá para recibir la respuesta.
4. **Genera un `correlation_id`** para poder asociar la respuesta a la petición original.
5. Define un **callback** `on_response` que:

   * Verifica que la respuesta coincide con el `correlation_id`.
   * Guarda el resultado en `response`.
6. Publica el mensaje con:

   * `reply_to`: cola temporal.
   * `correlation_id`: para emparejar.
7. Espera bloqueantemente con `connection.process_data_events()` hasta recibir la respuesta (ACK).
8. Devuelve respuesta al cliente HTTP.

### 🟢 Consumidor (hilo en background)

1. Se conecta a RabbitMQ con reintentos.
2. Declara la cola `mensajes` y comienza a consumir.
3. Cada vez que llega un mensaje:

   * Lo decodifica como `Evento`.
   * Procesa y guarda en memoria (`mensajes[]`).
   * Envía mensaje de respuesta a la `reply_to`, respetando el `correlation_id`.
   * Hace `basic_ack` para confirmar a RabbitMQ que el mensaje fue consumido.
4. Corre en un hilo separado para no bloquear FastAPI.

---

## ✅ ACK Nivel Aplicación vs. ACK AMQP

| Tipo ACK       | Quién lo gestiona           | Cómo se usa aquí                      |
| -------------- | --------------------------- | ------------------------------------- |
| **AMQP ACK**   | RabbitMQ (`basic_ack`)      | Consumidor llama `basic_ack` al final |
| **Aplicación** | Tú en tu código (reply\_to) | Se envía una respuesta al productor   |

En este caso usas **ambos**, lo cual es ideal:

* El consumidor le dice a RabbitMQ "ya he procesado el mensaje" (`basic_ack`).
* También le dice al **productor** "todo ok" con un mensaje personalizado de vuelta (`Evento {id} recibido`).

---

## 🧠 Perspectiva Hexagonal

Si quisieras hacer esto 100% hexagonal:

* `Evento` estaría en el dominio compartido.
* El `send_message` sería un **adaptador de entrada** (FastAPI).
* `pika` sería un **adaptador de salida** de un puerto tipo `MessageSenderPort`.
* El hilo consumidor sería otro **adaptador de entrada**, activado por RabbitMQ.
* El procesamiento del mensaje y la lógica de ACK formarían parte del caso de uso o dominio.

---

## 🧪 Ejemplo de flujo de prueba

```bash
curl -X POST http://localhost:8000/send \
     -H "Content-Type: application/json" \
     -d '{"id": "123", "tipo": "msg", "payload": {"data": "hola"}}'
```

Salida esperada en logs del productor:

```
📤 Evento enviado, esperando ACK...
✅ ACK recibido del consumidor: Evento 123 recibido y procesado.
```

Y en el consumidor:

```
📥 Recibido evento: msg con ID 123
📤 ACK enviado al productor: Evento 123 recibido y procesado.
```

---

