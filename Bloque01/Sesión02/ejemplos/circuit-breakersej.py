# main.py
from fastapi import FastAPI, Request, status, Header # Header añadido
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from typing import Optional, Any # Optional y Any añadidos

# --- 1. Tus Errores Personalizados (¡Hereda de Exception!) ---
class RecursoNoEncontradoError(Exception):
    def __init__(self, nombre_recurso: str, id_recurso: Any): # Usando Any como en tu ejemplo
        self.nombre_recurso = nombre_recurso
        self.id_recurso = id_recurso
        self.message = f"{nombre_recurso} con ID '{id_recurso}' no encontrado."
        self.error_code = f"{nombre_recurso.upper()}_NOT_FOUND"
        super().__init__(self.message)

class ReglaNegocioError(Exception):
    def __init__(self, message: str, error_code: str, context: dict = None):
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.message)

# --- NUEVA EXCEPCIÓN: AutenticacionFallidaError ---
class AutenticacionFallidaError(Exception):
    def __init__(self, message: str = "Autenticación fallida. Token inválido o ausente.", 
                 error_code: str = "AUTHENTICATION_FAILED"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

# --- 2. Tu App FastAPI ---
app = FastAPI(title="API Resiliente")

# --- Middleware para Trace ID (simplificado) ---
@app.middleware("http")
async def add_trace_id_middleware(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id # Guardamos en request.state
    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id
    return response

# --- 3. Tus Porteros (Exception Handlers) ---
@app.exception_handler(RecursoNoEncontradoError)
async def handle_recurso_no_encontrado(request: Request, exc: RecursoNoEncontradoError):
    trace_id = getattr(request.state, "trace_id", "N/A")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "trace_id": trace_id, "error_code": exc.error_code,
            "message": exc.message, "status_code": 404, "service_name": app.title,
            "context": {"recurso": exc.nombre_recurso, "id": exc.id_recurso}
        }
    )

@app.exception_handler(ReglaNegocioError)
async def handle_regla_negocio(request: Request, exc: ReglaNegocioError):
    trace_id = getattr(request.state, "trace_id", "N/A")
    status_code_http = status.HTTP_400_BAD_REQUEST
    if "EMAIL_ALREADY_EXISTS" in exc.error_code or "STOCK_INSUFFICIENTE" in exc.error_code:
        status_code_http = status.HTTP_409_CONFLICT

    return JSONResponse(
        status_code=status_code_http,
        content={
            "trace_id": trace_id, "error_code": exc.error_code,
            "message": exc.message, "status_code": status_code_http, "service_name": app.title,
            "context": exc.context
        }
    )

# --- NUEVO HANDLER para AutenticacionFallidaError ---
@app.exception_handler(AutenticacionFallidaError)
async def handle_autenticacion_fallida(request: Request, exc: AutenticacionFallidaError):
    trace_id = getattr(request.state, "trace_id", "N/A")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "trace_id": trace_id,
            "error_code": exc.error_code,
            "message": exc.message,
            "status_code": 401,
            "service_name": app.title
        }
    )

# --- Handler Genérico para 500 (¡El último recurso!) ---
@app.exception_handler(Exception)
async def handle_generic_exception(request: Request, exc: Exception):
    trace_id = getattr(request.state, "trace_id", "N/A")
    # En un entorno real, usa un logger configurado
    print(f"ERROR INESPERADO (RID: {trace_id}): {exc}", exc_info=True) 
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "trace_id": trace_id, "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Ocurrió un error inesperado en el servidor.",
            "status_code": 500, "service_name": app.title
        }
    )

# --- Tus Endpoints (que pueden lanzar estos errores) ---
db_items = {"item1": {"id": "item1", "nombre": "Poción de Salud"}, "item2": {"id": "item2", "nombre": "Espada de Luz"}}
db_users_emails = {"test@example.com"}

class UserCreate(BaseModel):
    email: str
    nombre: str

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    if item_id not in db_items:
        raise RecursoNoEncontradoError(nombre_recurso="Item", id_recurso=item_id)
    return db_items[item_id]

@app.post("/users")
async def create_user(user: UserCreate):
    if user.email in db_users_emails:
        raise ReglaNegocioError(
            message=f"El email '{user.email}' ya está registrado.",
            error_code="EMAIL_ALREADY_EXISTS",
            context={"email_conflictivo": user.email}
        )
    if not "@" in user.email:
        raise ReglaNegocioError(message="Formato de email inválido.", error_code="INVALID_EMAIL_FORMAT")

    import random
    if random.random() < 0.1: 
        raise ValueError("¡Algo explotó inesperadamente!")

    db_users_emails.add(user.email)
    return {"mensaje": f"Usuario {user.nombre} creado con email {user.email}"}
