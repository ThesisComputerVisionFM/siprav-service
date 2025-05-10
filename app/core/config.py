# app/core/config.py
from dotenv import load_dotenv # type: ignore
from pydantic_settings import BaseSettings # type: ignore
import os

# Carga las variables del archivo .env en el entorno
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret")


    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() # Crea una instancia para usarla en otros módulos

# Pequeña comprobación para asegurarnos de que la URL de la BD se cargó
if not settings.DATABASE_URL:
    print("Warning: DATABASE_URL not found in environment variables or .env file.")

# print(f"Loaded settings: DATABASE_URL='{settings.DATABASE_URL[:15]}...', SECRET_KEY='{settings.SECRET_KEY[:5]}...'") # Para depurar