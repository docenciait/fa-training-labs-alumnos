import os

class Settings:
    GRPC_SERVER: str = os.getenv("GRPC_SERVER", "todo-grpc")
    GRPC_PORT: int = int(os.getenv("GRPC_PORT", 50051))

settings = Settings()