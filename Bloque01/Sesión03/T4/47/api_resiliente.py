# app_resiliente.py (Versión Corregida SIN Deadlock)
from fastapi import FastAPI, HTTPException

# --- Estado Global Simulado ---
ESTADO_SERVICIOS = {
    "inventario": "ok"  # Puede ser 'ok' o 'roto'
}

app = FastAPI(title="Demostración de Resiliencia")


# --- Endpoints de Control (Nuestros "Interruptores") ---
# (Esta parte no cambia)
@app.post("/control/inventario/{estado}")
async def controlar_servicio_inventario(estado: str):
    """Permite cambiar el estado del servicio de inventario a 'ok' o 'roto'."""
    if estado in ["ok", "roto"]:
        ESTADO_SERVICIOS["inventario"] = estado
        return {"servicio": "inventario", "nuevo_estado": estado}
    raise HTTPException(status_code=400, detail="El estado solo puede ser 'ok' o 'roto'")


# --- Servicios Internos (Definidos como funciones normales) ---
# Ahora son funciones async normales, no necesariamente endpoints.
async def get_info_producto(producto_id: str):
    """Servicio CRÍTICO: Devuelve la info básica del producto."""
    # En un caso real, aquí podría haber una consulta a BBDD.
    return {"id": producto_id, "nombre": "Súper Poción", "descripcion": "Restaura 500 HP."}

async def get_stock_producto(producto_id: str):
    """Servicio NO CRÍTICO: Devuelve el stock. Puede fallar."""
    if ESTADO_SERVICIOS["inventario"] == "roto":
        # ¡Simulamos el fallo lanzando la misma excepción que lanzaría FastAPI!
        raise HTTPException(status_code=503, detail="Servicio de Inventario no disponible.")
    return {"producto_id": producto_id, "stock": 125}


# --- EL ENDPOINT PÚBLICO Y RESILIENTE (CORREGIDO) ---
@app.get("/producto/{producto_id}")
async def get_producto_completo(producto_id: str):
    """
    Endpoint resiliente que llama a las otras funciones directamente.
    """
    # 1. Obtener información principal (si esto falla, todo falla)
    # No necesitamos un try/except aquí, porque si la función crítica falla,
    # la excepción HTTPException se propagará y FastAPI la manejará correctamente.
    info_data = await get_info_producto(producto_id)
            
    # 2. Obtener stock (si esto falla, lo capturamos y continuamos)
    stock_data = {"stock": None, "aviso": "No se pudo verificar el stock en este momento."}
    try:
        # LLAMADA DIRECTA A LA FUNCIÓN
        stock_data = await get_stock_producto(producto_id)
    except HTTPException:
        # ¡LA MAGIA DE LA RESILIENCIA!
        # Si get_stock_producto lanza la excepción, la capturamos aquí
        # y usamos los datos de fallback sin que el endpoint principal falle.
        pass
            
    # 3. Combinar y devolver la respuesta
    return {
        "informacion_principal": info_data,
        "disponibilidad": stock_data
    }