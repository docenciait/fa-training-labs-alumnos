## Parte 1: Apache Kafka - La Plataforma de Streaming de Eventos

### ¿Qué es Apache Kafka?

Imagina a Kafka no como una simple cola de mensajes, sino como el **sistema nervioso central de datos** de una organización. Es una **plataforma de streaming de eventos distribuida, tolerante a fallos y de alto rendimiento**.

En lugar de simplemente enviar un mensaje de un punto A a un punto B, Kafka está diseñado para manejar **flujos continuos de eventos** (streams) y almacenarlos de forma duradera. Un "evento" es cualquier cosa que sucede en tu negocio: un clic en una página web, una venta realizada, una lectura de un sensor de IoT, una transacción financiera, etc.

Kafka te permite:
1.  **Publicar y Suscribirte (Pub/Sub):** Múltiples aplicaciones (productores) pueden enviar eventos a Kafka, y múltiples aplicaciones (consumidores) pueden leerlos en tiempo real.
2.  **Almacenar:** Guarda los flujos de eventos de forma segura y duradera por el tiempo que necesites (desde minutos hasta años). Esto es clave: puedes "rebobinar" y volver a procesar eventos pasados.
3.  **Procesar:** Permite el procesamiento de flujos de eventos en tiempo real, ya sea con aplicaciones externas o con la librería Kafka Streams.

### Conceptos Clave de Kafka

Para entender cómo funciona, necesitas conocer su terminología:

* **Evento (o Mensaje):** La unidad de datos en Kafka. Consiste en una clave (opcional), un valor (el dato en sí), una marca de tiempo y metadatos.
* **Topic (Tema):** Es una categoría o un "feed" al que se envían los eventos. Piensa en ello como una tabla en una base de datos o una carpeta en un sistema de archivos. En tu código, el topic es `"eventos"`.
* **Partición (Partition):** La clave de la escalabilidad de Kafka. Un topic se divide en una o más particiones. Cada partición es un **log de eventos ordenado e inmutable**. Los nuevos eventos se añaden siempre al final. Kafka garantiza el orden de los mensajes *dentro de una misma partición*, pero no entre particiones diferentes de un mismo topic.
* **Offset:** Un número secuencial único que identifica a cada evento dentro de una partición. Los consumidores utilizan este offset para saber qué mensajes ya han leído.
* **Broker:** Un servidor de Kafka. Un clúster de Kafka se compone de varios brokers que trabajan juntos para proporcionar escalabilidad y tolerancia a fallos.
* **Productor (Producer):** Una aplicación que escribe (publica) eventos en uno o más topics de Kafka. Tu `producer.py` es un productor.
* **Consumidor (Consumer):** Una aplicación que lee (se suscribe) a uno o más topics. Tu `consumer.py` es un consumidor.
* **Grupo de Consumidores (Consumer Group):** Un conjunto de consumidores que trabajan juntos para leer un topic. Kafka distribuye las particiones del topic entre los consumidores del grupo. Así, si un topic tiene 4 particiones y tu grupo tiene 4 consumidores, cada uno leerá de una partición, logrando un paralelismo perfecto. Si un consumidor se cae, Kafka reasigna su partición a otro miembro del grupo.

---

## Parte 2: Opciones de Configuración Clave

En tu código usas varias opciones importantes:

* `bootstrap_servers`: Es la lista de brokers a los que el cliente (productor o consumidor) se conectará inicialmente para descubrir el resto del clúster. No necesita ser la lista completa, solo uno o dos para arrancar.
* `group_id`: Identificador único para un grupo de consumidores. Es **esencial** para la escalabilidad. Todos los consumidores con el mismo `group_id` pertenecen al mismo grupo y se reparten las particiones de un topic. Si dos consumidores tienen `group_id` diferentes, ambos recibirán **todos** los mensajes del topic (comportamiento de broadcast).
* `auto_offset_reset`: Define qué hacer cuando un consumidor de un nuevo grupo se conecta por primera vez y no hay un offset guardado para él.
    * `"earliest"` (el que usas): El consumidor empezará a leer desde el **primer mensaje disponible** en la partición. Muy útil para desarrollo y para procesar datos históricos.
    * `"latest"` (el valor por defecto): El consumidor empezará a leer solo los **nuevos mensajes** que lleguen después de que se conecte. Ideal para procesar datos en tiempo real sin importar el pasado.

---

## Parte 3: Kafka vs. RabbitMQ - Una Comparativa

Esta es una pregunta muy común. Ambos son sistemas de mensajería excelentes, pero con filosofías y casos de uso diferentes.

| Característica        | Apache Kafka                                                                                                              | RabbitMQ                                                                                                                        |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------ |
| **Arquitectura** | **Log de Eventos Distribuido:** Se basa en un log inmutable y replicado. Los mensajes no se eliminan al ser leídos, se retienen según una política. | **Broker de Mensajes Tradicional:** Se basa en colas. Los mensajes se eliminan de la cola una vez que son consumidos y confirmados (ACK). |
| **Modelo** | **Pub/Sub a gran escala.** Ideal para difundir datos a múltiples consumidores o sistemas de forma masiva.                       | **Flexible.** Soporta Pub/Sub, colas de trabajo, enrutamiento complejo (topic, fanout, direct exchanges), RPC, etc. Es un "smart broker". |
| **Rendimiento** | **Rendimiento extremadamente alto** (millones de mensajes/seg). Optimizado para I/O secuencial y batching.                  | **Buen rendimiento** (decenas o cientos de miles de mensajes/seg). Más enfocado en la flexibilidad de enrutamiento que en el throughput bruto. |
| **Persistencia** | **Retención a largo plazo.** Los datos pueden persistir durante días, meses o para siempre. Actúa como un sistema de almacenamiento. | **Persistencia a corto plazo.** Diseñado para actuar como un búfer temporal para los mensajes hasta que son consumidos.                     |
| **Consumidores** | **"Dumb consumers".** La lógica reside en los consumidores, que son responsables de llevar la cuenta de su offset (posición) en el log. | **"Smart broker".** El broker es responsable de empujar los mensajes a los consumidores y gestionar el estado de la cola.                  |
| **Casos de Uso** | - Streaming de datos a gran escala<br>- Análisis en tiempo real<br>- Ingesta de logs y métricas<br>- Sincronización de bases de datos (CDC)<br>- Desacoplamiento de microservicios (event-driven) | - Colas de tareas (task queues)<br>- Enrutamiento de mensajes complejo<br>- Notificaciones a sistemas específicos<br>- Desacoplamiento de microservicios (command-driven) |
| **Conclusión** | **Plataforma de streaming** para pipelines de datos.                                                                       | **Broker de mensajes** para integración de aplicaciones.                                                                        |

---

## Parte 4: Análisis del Código

Ahora, vamos a desglosar tu código. Está muy bien estructurado y sigue buenas prácticas.

### `producer.py` - El que Envía los Eventos

```python
# Importaciones necesarias: FastAPI para la API web, el modelo Pydantic,
# el productor asíncrono de aiokafka, asyncio para tareas asíncronas
# y json para la serialización.
from fastapi import FastAPI
from models import Evento
from aiokafka import AIOKafkaProducer
import asyncio
import json
import logging # Aunque importado, no se usa. Sería bueno para logs más formales.

# Se crea la instancia de la aplicación FastAPI.
app = FastAPI()

# Se inicializa la variable global para el productor. Es 'None' al principio.
producer: AIOKafkaProducer = None

# Constantes para la configuración. Es una buena práctica para mantener el código limpio.
BOOTSTRAP_SERVERS = "kafka:9092" # "kafka" es el nombre del servicio en Docker Compose.
TOPIC = "eventos"

# Esta función es CRÍTICA. Se encarga de crear y conectar el productor a Kafka.
async def get_kafka_producer():
    global producer
    retries = 10 # Número de intentos de conexión.
    
    # Bucle de reintentos: muy importante en arquitecturas de microservicios (ej. Docker),
    # donde este servicio puede arrancar ANTES de que el broker de Kafka esté listo.
    for i in range(retries):
        try:
            # Se instancia el productor, pasándole la dirección de los brokers.
            producer = AIOKafkaProducer(
                bootstrap_servers=BOOTSTRAP_SERVERS
            )
            # Inicia el productor. Esta es una operación de red, por lo que es asíncrona.
            # Establece la conexión y obtiene metadatos del clúster.
            await producer.start()
            print("✅ Productor Kafka iniciado correctamente.")
            return # Si tiene éxito, sale de la función.
        except Exception as e:
            # Si la conexión falla (ej. Kafka no está listo), lo imprime y espera.
            print(f"❌ Reintentando conexión a Kafka ({i+1}/{retries}): {e}")
            await asyncio.sleep(3) # Espera 3 segundos antes del siguiente intento.
            
    # Si después de todos los reintentos no se pudo conectar, lanza un error para detener la aplicación.
    raise RuntimeError("🛑 No se pudo conectar a Kafka.")

# Decorador de FastAPI que ejecuta esta función cuando la aplicación arranca.
# Asegura que el productor esté listo antes de aceptar peticiones.
@app.on_event("startup")
async def startup_event():
    await get_kafka_producer()

# Decorador que se ejecuta cuando la aplicación se apaga (ej. con Ctrl+C).
# Es crucial para cerrar las conexiones de forma limpia.
@app.on_event("shutdown")
async def shutdown_event():
    if producer:
        # Detiene el productor, enviando los mensajes pendientes y cerrando conexiones.
        await producer.stop()

# El endpoint de la API que recibe los eventos a través de una petición POST.
@app.post("/send")
async def send_message(evento: Evento):
    # Serializa el objeto Pydantic 'Evento' a un diccionario, luego a un string JSON,
    # y finalmente lo codifica a bytes (UTF-8), que es el formato que Kafka espera.
    value = json.dumps(evento.dict()).encode("utf-8")
    
    # Envía el mensaje al topic especificado.
    # 'send_and_wait' es un método conveniente que espera la confirmación (ACK) del broker
    # de que el mensaje ha sido recibido y escrito en la partición.
    # Esto garantiza la entrega pero puede ser un poco más lento que solo 'send()'.
    await producer.send_and_wait(TOPIC, value=value)
    
    # Devuelve una respuesta confirmando el envío.
    return {"status": "message sent", "evento": evento}
```

### `consumer.py` - El que Lee los Eventos

```python
# Importaciones similares al productor, pero ahora con AIOKafkaConsumer.
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from models import Evento
import json
import asyncio

app = FastAPI()

# Una lista en memoria para guardar los mensajes recibidos.
# En una aplicación real, aquí harías algo más útil: guardar en una base de datos,
# procesar los datos, llamar a otra API, etc.
mensajes: list[Evento] = []

# Constantes de configuración.
KAFKA_BOOTSTRAP = "kafka:9092"
TOPIC = "eventos"

# Esta es la función principal del consumidor. Se ejecutará en un bucle infinito.
async def consume():
    # Se instancia el consumidor.
    consumer = AIOKafkaConsumer(
        TOPIC, # El topic (o lista de topics) al que se suscribe.
        bootstrap_servers=KAFKA_BOOTSTRAP,
        # MUY IMPORTANTE: Identifica al consumidor como parte de este grupo.
        # Permite escalar ejecutando varias instancias de este mismo servicio.
        group_id="grupo-consumidor-2", 
        # Como se explicó antes, empieza a leer desde el principio del topic.
        auto_offset_reset="earliest" 
    )
    # Inicia el consumidor y se conecta al clúster de Kafka.
    await consumer.start()
    try:
        # Este es el bucle de consumo. 'async for' es una forma elegante y eficiente
        # de esperar y procesar mensajes a medida que llegan, sin bloquear el hilo.
        async for msg in consumer:
            # 'msg.value' contiene el mensaje en bytes. Se decodifica a string.
            data = json.loads(msg.value.decode())
            # Se convierte el diccionario JSON de vuelta a un objeto Pydantic 'Evento'.
            # Esto valida que el mensaje tiene la estructura esperada.
            evento = Evento(**data)
            
            # Imprime el evento recibido.
            print(f"📥 Recibido evento: {evento.tipo} con ID {evento.id}")
            
            # Añade el evento a la lista en memoria.
            mensajes.append(evento)
    finally:
        # Este bloque se asegura de que, si el bucle termina por cualquier razón
        # (aunque en este caso no debería), el consumidor se detenga limpiamente.
        await consumer.stop()

# En el evento de arranque de la aplicación FastAPI...
@app.on_event("startup")
async def startup_event():
    # ...se crea una tarea en segundo plano para ejecutar la función 'consume'.
    # asyncio.create_task() es VITAL aquí. Lanza el bucle de consumo para que se ejecute
    # concurrentemente, sin bloquear el arranque del servidor web de FastAPI.
    # Así, la API puede servir peticiones (como /messages) mientras consume de Kafka.
    asyncio.create_task(consume())

# Un endpoint de prueba para ver los mensajes que se han consumido.
@app.get("/messages")
async def get_messages():
    # Devuelve el contenido de la lista 'mensajes'.
    return [m.dict() for m in mensajes]
