# main_sec_5_1.py
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# --- 1. Configuración de Seguridad ---
SECRET_KEY = "mi-clave-secreta-para-el-ejemplo-de-jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- 2. Utilidades para Contraseñas y Tokens ---
# pwd_context es el gestor de passwords y oauth2_scheme es el extractor de tokens
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Le dice a FastAPI dónde está el endpoint de login

# --- 3. Base de Datos Ficticia de Usuarios ---
# En un caso real, esto vendría de una base de datos.
fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "Usuario Uno",
        "email": "user1@example.com",
        "hashed_password": pwd_context.hash("pass123"), # La contraseña "pass123" hasheada
    }
}

# --- 4. Funciones de Creación y Verificación de JWT ---
def create_access_token(data: dict):
    to_encode = data.copy() # Copiamos por seguridad
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # le paso el claim exp
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # codificadmos el token
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Esta es la dependencia "guardián". Se encarga de:
    1. Extraer el token de la cabecera 'Authorization'.
    2. Decodificarlo y validar su firma y expiración.
    3. Devolver los datos del usuario si todo es correcto.
    4. Lanzar una excepción si algo falla.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificamos el token con la secret key y el algoritmo consecuente
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = fake_users_db.get(username) # sacamos el usuario de la db (fake)
    
    if user is None:
        raise credentials_exception
    return user

# --- 5. La Aplicación FastAPI ---
app = FastAPI()

# form_data: OAuth2PasswordRequestForm = Depends() Permite que si no se le pasa
# formulario con los datos de usuario password no sigue

@app.post("/token", summary="Iniciar sesión y obtener un token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_in_db = fake_users_db.get(form_data.username)
    # Sí, la siguiente condición nos dice si el usuario y password son correctos
    if not user_in_db or not pwd_context.verify(form_data.password, user_in_db["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    # El "sub" (subject) es el identificador único del usuario en el token.
    access_token = create_access_token(data={"sub": user_in_db["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", summary="Obtener perfil del usuario actual (protegido)")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    # Gracias a `Depends(get_current_user)`, este código solo se ejecuta
    # si el token es válido. `current_user` contendrá los datos del usuario.
    # Eliminamos el hash de la contraseña antes de devolver los datos.
    user_info = current_user.copy()
    user_info.pop("hashed_password")
    return user_info