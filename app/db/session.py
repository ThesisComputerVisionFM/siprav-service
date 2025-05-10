# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings # Importa la configuración

# Crea el motor de SQLAlchemy usando la URL de la configuración
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Crea una factoría de sesiones configurada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea la base para los modelos ORM
Base = declarative_base()

# Función para obtener una sesión de base de datos (usada como dependencia en FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print(f"SQLAlchemy engine created for: {str(engine.url).split('@')[-1]}") # Verifica que el motor se creó
