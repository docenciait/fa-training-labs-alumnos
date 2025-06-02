import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.config import settings

MAX_RETRIES = 10
SLEEP_INTERVAL = 3  # seconds

for i in range(MAX_RETRIES):
    try:
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
        conn = engine.connect()
        conn.close()
        break
    except OperationalError:
        print(f"❌ Intento {i+1}: MariaDB no disponible, reintentando en {SLEEP_INTERVAL} segundos...")
        time.sleep(SLEEP_INTERVAL)
else:
    print("❌ No se pudo conectar a MariaDB después de varios intentos. Abortando.")
    raise RuntimeError("No se pudo conectar a MariaDB.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
