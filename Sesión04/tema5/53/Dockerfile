# Usamos una imagen oficial de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el fichero de requisitos e instalamos las dependencias
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiamos el código de nuestra aplicación
COPY ./main_sec_5_2.py .

# El comando que se ejecutará cuando el contenedor arranque
# --host 0.0.0.0 es crucial para que sea accesible desde otros contenedores
CMD ["uvicorn", "main_sec_5_2:app", "--host", "0.0.0.0", "--port", "8000"]