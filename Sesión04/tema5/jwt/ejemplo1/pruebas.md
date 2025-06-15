
# 🔥 PRUEBAS COMPLETAS

**Suposición:**

* Backend corriendo en `http://localhost:8000`
* Usuario de prueba en la “base de datos”:

  * `username=user1`
  * `password=password123`

---

### 1️⃣ **Login** — Obtener Access Token + Refresh Token

```bash
curl -X POST http://localhost:8000/token \
  -d "username=user1&password=password123" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

🧩 **Respuesta esperada**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
  "token_type": "bearer"
}
```

* Guarda el `access_token` y el `refresh_token`.

---

### 2️⃣ **Access Token válido** — Obtener Perfil

```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer <access_token>"
```

🧩 **Respuesta esperada**:

```json
{
  "user": {
    "sub": "user1",
    "roles": [
      "user"
    ],
    "exp": 1715294732
  }
}
```

✅ El servidor valida tu token correctamente y recupera la información.

---

### 3️⃣ **Refresh Token** — Obtener nuevo Access Token

⚠️ **Simular** que el `access_token` ha caducado (o simplemente refrescar):

```bash
curl -X POST http://localhost:8000/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

🧩 **Respuesta esperada**:

```json
{
  "access_token": "nuevo_access_token....",
  "refresh_token": "nuevo_refresh_token....",
  "token_type": "bearer"
}
```

✅ Tokens renovados correctamente.

---

### 4️⃣ **Logout** — Invalida el Refresh Token

```bash
curl -X POST http://localhost:8000/logout \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

🧩 **Respuesta esperada**:

```json
{
  "detail": "Logged out successfully"
}
```

✅ El `refresh_token` ha sido invalidado.

---

### 5️⃣ **Reutilizar Refresh Token inválido** (después del logout)

```bash
curl -X POST http://localhost:8000/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<mismo_refresh_token>"}'
```

🧩 **Respuesta esperada**:

```json
{
  "detail": "Refresh token invalid or revoked"
}
```

✅ **El token fue revocado correctamente**.

---

# 🛠️ Pequeño Script para probar todo junto (opcional)

```bash
# Login
resp=$(curl -s -X POST http://localhost:8000/token -d "username=user1&password=password123" -H "Content-Type: application/x-www-form-urlencoded")
access_token=$(echo $resp | jq -r .access_token)
refresh_token=$(echo $resp | jq -r .refresh_token)

# Ver perfil
curl -s -X GET http://localhost:8000/users/me -H "Authorization: Bearer $access_token" | jq

# Refresh token
curl -s -X POST http://localhost:8000/refresh -H "Content-Type: application/json" -d "{\"refresh_token\":\"$refresh_token\"}" | jq

# Logout
curl -s -X POST http://localhost:8000/logout -H "Content-Type: application/json" -d "{\"refresh_token\":\"$refresh_token\"}" | jq
```

---

# 🚀 **Estado del Proyecto**

✅ Login funcionando.
✅ Access token protege endpoints.
✅ Refresh de token funcionando.
✅ Logout invalidando el refresh token.
✅ **Sin errores ni warnings** tras ajustar `bcrypt==3.2.0`.

---

¿Quieres que ahora te arme un `docker-compose.yml` con PostgreSQL simulando un user-service para que quede más parecido a un microservicio real? 🐳✨
