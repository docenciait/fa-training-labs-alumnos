# main_sec_5_2.py
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# --- Configuración (sin cambios) ---
SECRET_KEY = "mi-clave-secreta-para-el-ejemplo-de-jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Base de Datos Ficticia  ---
fake_users_db = {
    "user_viewer": {
        "username": "user_viewer",
        "full_name": "Usuario Lector",
        "email": "viewer@example.com",
        "hashed_password": pwd_context.hash("pass123"),
        "roles": ["viewer"],
        "scopes": ["items:read"], # Solo puede leer
    },
    "user_editor": {
        "username": "user_editor",
        "full_name": "Usuario Editor",
        "email": "editor@example.com",
        "hashed_password": pwd_context.hash("pass456"),
        "roles": ["editor"],
        "scopes": ["items:read", "items:write"], # Puede leer y escribir
    }
}

# --- Funciones de JWT (create_access_token sin cambios) ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependencias de Seguridad (get_current_user ahora extrae más claims) ---
async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # Extraemos los scopes del payload del token
        scopes = payload.get("scopes", [])
        
    except JWTError:
        raise credentials_exception
    
    # Devolvemos un diccionario con los datos del usuario del token
    return {"username": username, "scopes": scopes}


# --- NUEVA Dependencia de AUTORIZACIÓN ---
def require_scope(required_scope: str):
    """
    Esta es una factoría de dependencias. Devuelve una función 'checker'
    que verifica si el scope requerido está en la lista de scopes del usuario.
    """
    async def scope_checker(current_user: dict = Depends(get_current_user_from_token)):
        if required_scope not in current_user.get("scopes", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Se requiere el scope: '{required_scope}'"
            )
        return current_user
    return scope_checker

# --- Aplicación FastAPI ---
app = FastAPI()

# El endpoint de login ahora debe incluir los scopes en el token
@app.post("/token", summary="Iniciar sesión para obtener un token con scopes")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_in_db = fake_users_db.get(form_data.username)
    if not user_in_db or not pwd_context.verify(form_data.password, user_in_db["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    
    # Creamos el token incluyendo el username (sub) y sus scopes
    access_token = create_access_token(
        data={"sub": user_in_db["username"], "scopes": user_in_db["scopes"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Endpoints Protegidos por Scopes ---
@app.get("/items", summary="Leer lista de items (requiere scope 'items:read')")
async def read_items(current_user: dict = Depends(require_scope("items:read"))):
    return [{"id": 1, "name": "Poción de Salud"}, {"id": 2, "name": "Espada Mágica"}]

@app.post("/items", summary="Crear un item (requiere scope 'items:write')")
async def create_item(current_user: dict = Depends(require_scope("items:write"))):
    return {"status": "success", "message": f"Item creado por el usuario '{current_user['username']}'"}