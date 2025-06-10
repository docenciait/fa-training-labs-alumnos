¡Perfecto! Aquí tienes la estructura inicial del laboratorio como la venimos haciendo, todo bien profesional para que se pueda integrar en tu curso:

---

# 🔹 LAB 4 – Seguridad Básica con JWT, CORS y Resiliencia

| Ítem                | Detalles                                                                                                                                     |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 🕒 **Duración**     | 1.5 h                                                                                                                                        |
| 🎯 **Objetivo**     | Añadir autenticación JWT, configurar CORS de manera segura y aplicar un circuito de resiliencia en FastAPI                                   |
| 🧠 **Temas**        | Tema 5 completo (Seguridad y Resiliencia en Microservicios)                                                                                  |
| ⚙️ **Tecnologías**  | FastAPI, PyJWT, FastAPI-JWT-Auth, Pydantic, FastAPI CORS Middleware, PyBreaker                                                               |
| 📁 **Entregable**   | Sistema protegido con login, generación de tokens JWT, autorización por scope, CORS configurado y un Circuit Breaker para servicios externos |
| 🧪 **Tareas clave** |                                                                                                                                              |

* Generar y validar JWT (login, registro ficticio).
* Proteger endpoints mediante autorización por scope.
* Configurar CORS de forma segura.
* Implementar un Circuit Breaker para invocaciones HTTP externas (simulación).

\| 🧩 **Repositorio** | `lab04-seguridad` |

---

## ✅ Enunciado

Desarrolla una pequeña API REST en **FastAPI** que gestione usuarios ficticios y permita proteger los endpoints usando **JWT** con scopes específicos.

Además, configura CORS correctamente para que solo orígenes seguros puedan acceder. Finalmente, añade resiliencia a una llamada simulada a un servicio externo aplicando un patrón **Circuit Breaker**.

El servicio debe permitir:

* Registro de un usuario ficticio (no es necesario persistir en DB, usa memoria).
* Login que genere un **JWT** válido.
* Endpoints protegidos por scopes:

  * `GET /profile`: requiere scope `profile`.
  * `GET /admin`: requiere scope `admin`.
* Configuración de CORS para aceptar solo un dominio permitido.
* Simular una llamada externa protegida por **Circuit Breaker**.

### 🎯 Requisitos específicos

1. **Login**: Entrega JWT firmado usando `HS256`.
2. **Scopes**: Define scopes en el token y protégete contra accesos no autorizados.
3. **CORS**: Permitir solo peticiones desde `http://localhost:3000`.
4. **Circuit Breaker**:

   * Simula una llamada HTTP (por ejemplo, a `https://dummyjson.com/users/1`).
   * Implementa un Circuit Breaker que abra el circuito si fallan 3 intentos consecutivos.
5. **Validaciones**:

   * Usuario y contraseña deben ser validados (aunque sea hardcodeado).

---

## 🚀 Instrucciones

### 1. Clona el repositorio base:

```bash
git clone https://github.com/curso-imagina/lab04-seguridad-inicial.git
cd lab04-seguridad-inicial
```

### 2. Levanta el entorno:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### 3. Crea la API siguiendo los pasos:

* Crea los endpoints `/items`, `/login`, `/profile`, `/admin`.
* Implementa JWT con scopes. 
* Configura correctamente CORS.
* Añade un Circuit Breaker a un endpoint `/external-data`.

### 4. Prueba con:

```bash
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "secret"}'
```

Guarda el token y úsalo para acceder a:

```bash
curl -X GET http://localhost:8000/profile -H "Authorization: Bearer <token>"
```

---

## 📚 Pistas y Documentación

* [FastAPI JWT Auth](https://indominusbyte.github.io/fastapi-jwt-auth/)
* [CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/)
* [PyBreaker](https://pybreaker.readthedocs.io/en/latest/)

---

## 🎁 Entregable

Un repositorio con:

* Código limpio y documentado.
* Archivo `requirements.txt` actualizado.
* Configuración CORS correcta.
* Circuit Breaker implementado en una llamada simulada.
* Pruebas manuales de login y acceso protegido.
* Ejemplos de error al activar el Circuit Breaker.

---

## 📁 Estructura esperada del Repositorio Final

```
lab04-seguridad-final/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── models.py
│   ├── schemas.py
│   ├── dependencies.py
│   └── external.py
├── requirements.txt
├── README.md
```

---

