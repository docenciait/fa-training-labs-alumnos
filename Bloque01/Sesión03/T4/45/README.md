
---

### 💥 **Ahora qué pasa**

✅ Lanzas **una llamada**:

```bash
curl http://localhost:8000/call-service/
```

Y en **consola de cliente retry** verás:

```
WARNING:root:503 Service Unavailable, reintentando...
WARNING:root:503 Service Unavailable, reintentando...
```

Si después de 3 intentos no puede → devuelve:

```json
{
  "detail": "Servicio no disponible después de varios intentos"
}
```

✅ Si en algún intento hay 200 OK, devuelve:

```json
{
  "result": {
    "message": "Service OK"
  }
}
```



* Cada vez que entres al `call-service`, FastAPI hará el retry **internamente** si ve un 503.
* La **cantidad de llamadas** al `/fake_service` son muchas porque probablemente:

  * Otros clientes (Postman, navegador, herramientas) están llamando.
  * Fake service siempre responde 503 o 200 random.

✅ **NO confundir** logs de servidor con los **retries internos** de **tu única llamada**.

---

# 🛠️ **¿Qué logramos ahora?**

* **Simple**: `raise Exception` en 503 para que Tenacity retrigger.
* **Claro**: `wait_fixed` de 2 segundos entre reintentos.
* **Visible**: Logs en consola de reintentos.

