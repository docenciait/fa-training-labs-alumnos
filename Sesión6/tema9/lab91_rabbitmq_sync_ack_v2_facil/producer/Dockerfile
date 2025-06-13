FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir fastapi uvicorn pika
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
