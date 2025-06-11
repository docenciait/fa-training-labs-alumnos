
# 🎯 Reto del Alumno – Extensión DDD en el Microservicio de Órdenes

## 🧠 Objetivo

Ampliar el microservicio existente incorporando una nueva funcionalidad de **gestión de pagos** (`Payment`) utilizando **Domain-Driven Design**. Esta nueva funcionalidad debe reflejar claramente:

* Nuevas entidades y value objects
* Eventos de dominio que comuniquen el estado del negocio
* Servicios de dominio que encapsulen lógica significativa
* Puertos bien definidos para entrada (casos de uso) y salida (persistencia)
* DTOs para aislar dominio e infraestructura
* Lenguaje ubicuo respetado en todo el diseño

---

## 🧩 Enunciado

**Contexto:**
Cuando un cliente realiza una orden, puede pagarla posteriormente. El sistema debe permitir:

* **Registrar un pago** para una orden existente.
* **Verificar** si el pago es válido (importe exacto).
* **Notificar internamente** que una orden ha sido pagada.

---

## 📚 Requisitos del reto

### ✅ 1. Entidad de dominio: `Payment`

* Representa un pago vinculado a una orden.
* Atributos:

  * `id: UUID`
  * `order_id: UUID`
  * `amount: float`
  * `method: str`
  * `timestamp: datetime`

### ✅ 2. Value Object: `Money`

* Representa un valor monetario (con validación y comparación).
* Atributos:

  * `amount: float`
  * `currency: str`

### ✅ 3. Evento de dominio

* `PaymentReceivedEvent`: generado al registrar exitosamente un pago.

### ✅ 4. Servicio de Dominio (opcional)

* Si decides que la validación del importe o estado del pago no pertenece a `Payment`, encapsúlala en un servicio de dominio: `PaymentValidatorService`.

### ✅ 5. Puerto de entrada

* Interfaz `PaymentServicePort` con método `register_payment(PaymentCreateDTO) -> PaymentDTO`.

### ✅ 6. Puerto de salida

* Interfaz `PaymentRepositoryPort` con métodos `save(payment)` y `find_by_order_id(order_id)`.

### ✅ 7. DTOs

* `PaymentCreateDTO` para recibir datos desde la API.
* `PaymentDTO` para devolver al cliente.

### ✅ 8. Lenguaje Ubicuo

Usa términos del dominio como:

* `register_payment`, `PaymentReceived`, `amount`, `method`, `paid_at`, `is_valid_amount()`

---

## 🚀 Actividad esperada

* Crear la entidad `Payment` y VO `Money` en `domain/`
* Crear evento `PaymentReceivedEvent`
* Definir puerto `PaymentServicePort` (entrada) y `PaymentRepositoryPort` (salida) en `application/ports`
* Implementar `PaymentApplicationService` en `application/services`
* Implementar `MariaDBPaymentRepository` en `infrastructure/repositories`
* Crear los DTOs en `application/dtos`
* Añadir endpoints en `/payments` con POST y GET
* Inyectar dependencias en `dependencies.py`

---

## 🧪 Bonus

* Añadir prueba con `curl` para registrar un pago:

```bash
curl -X POST http://localhost:8000/payments \
 -H 'Content-Type: application/json' \
 -d '{"order_id": "...", "amount": 49.99, "method": "credit_card"}'
```

---

## 🧠 Preguntas de reflexión

1. ¿Dónde colocaste la validación del importe del pago: en la entidad o en un servicio? ¿Por qué?
2. ¿Qué pasa si se duplica un pago? ¿Cómo protegerías el dominio?
3. ¿Qué ocurriría si más adelante quieres emitir un evento a Kafka desde el evento de dominio?
4. ¿Qué otras funcionalidades relacionadas con pagos podrías implementar con esta base?

---

¿Quieres que te prepare también un repositorio base vacío con esta estructura para los alumnos? ¿O prefieres que redacte la solución como guía del profesor?
