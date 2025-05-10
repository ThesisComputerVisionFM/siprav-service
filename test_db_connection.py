import os
from sqlalchemy import create_engine, text # Import text para SQL directo
from sqlalchemy.exc import SQLAlchemyError # Para errores específicos de SQLAlchemy
from dotenv import load_dotenv
import sys

def test_db_connection():
    print("--- Iniciando prueba de conexión a la Base de Datos ---")

    # Determina la ruta base (asumiendo que este script está en 'backend/')
    # Si mueves el script, ajusta esto.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(BASE_DIR, '.env')

    print(f"Buscando archivo .env en: {dotenv_path}")

    # Carga variables desde el archivo .env especificado
    loaded = load_dotenv(dotenv_path=dotenv_path)

    if not loaded:
        print("ADVERTENCIA: No se pudo cargar el archivo .env. Asegúrate de que exista en la carpeta 'backend/'.")

    # Obtiene la DATABASE_URL del entorno
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("\nERROR CRÍTICO: La variable de entorno DATABASE_URL no se encontró.")
        print("Verifica que esté definida en tu archivo .env y que el archivo .env se haya cargado.")
        sys.exit(1) # Termina el script si no hay URL

    # Muestra parte de la URL para verificación (ocultando info sensible)
    try:
        parts = DATABASE_URL.split('@')
        user_part = parts[0].split('//')[-1].split(':')[0]
        server_part = parts[1].split('/')[0]
        db_part = parts[1].split('/')[1].split('?')[0]
        driver_part = DATABASE_URL.split('driver=')[-1] if 'driver=' in DATABASE_URL else '[Driver no especificado]'
        print(f"\nURL encontrada: mssql+pyodbc://{user_part}:***@{server_part}/{db_part}?driver={driver_part}")
    except IndexError:
        print(f"\nURL encontrada (formato no estándar o incompleto, mostrando inicio): {DATABASE_URL[:20]}...")

    print("\nIntentando crear motor SQLAlchemy...")

    try:
        # Crea el motor. echo=True mostrará el SQL generado (útil para depurar)
        # pool_pre_ping=True es bueno para conexiones de larga duración
        engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

        print("Motor creado exitosamente.")
        print("Intentando establecer conexión y ejecutar 'SELECT 1'...")

        # Intenta conectar y ejecutar una consulta simple
        # Usar 'with' asegura que la conexión se cierre automáticamente
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            scalar_result = result.scalar() # Obtiene el primer valor de la primera fila
            print(f"Consulta 'SELECT 1' ejecutada. Resultado: {scalar_result}")

        # Si llegamos aquí, todo funcionó
        print("\n*****************************************************")
        print("*** ¡CONEXIÓN EXITOSA! La DATABASE_URL es válida. ***")
        print("*****************************************************\n")

    except ImportError as e:
        print("\n--- ERROR DE CONEXIÓN ---")
        print(f"ImportError: {e}")
        print("Causa probable: El controlador 'pyodbc' no está instalado correctamente")
        print("o falta el driver ODBC de Microsoft SQL Server en tu sistema operativo.")
        print("Asegúrate de haber ejecutado 'pip install pyodbc' en tu entorno virtual")
        print("y de tener instalado 'ODBC Driver for SQL Server'.")

    except SQLAlchemyError as e:
        # Errores específicos de SQLAlchemy (más comunes para conexión)
        print("\n--- ERROR DE CONEXIÓN (SQLAlchemyError) ---")
        print(f"Error: {e}")
        print("\nCausas probables:")
        print("  - Nombre de servidor, base de datos, usuario o contraseña incorrectos en DATABASE_URL.")
        print("  - El servicio de SQL Server no se está ejecutando en el servidor especificado.")
        print("  - Firewall bloqueando la conexión al puerto de SQL Server (generalmente 1433).")
        print("  - Nombre del driver ODBC incorrecto en la parte '?driver=...' de la URL.")
        print("  - Problemas de conectividad de red.")
        print("  - La base de datos especificada no existe en el servidor.")

    except Exception as e:
        # Otros errores inesperados
        print("\n--- ERROR INESPERADO ---")
        print(f"Ocurrió un error no específico de SQLAlchemy: {e}")
        print("Revisa la traza completa y la configuración.")

    finally:
        print("\n--- Prueba de conexión finalizada. ---")

# Ejecuta la función de prueba cuando se corre el script
if __name__ == "__main__":
    test_db_connection()