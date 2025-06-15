import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@mariadb:3306/tododb")

settings = Settings()