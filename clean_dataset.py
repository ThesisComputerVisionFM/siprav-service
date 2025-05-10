import os
from PIL import Image, UnidentifiedImageError

# Ruta de la carpeta con imágenes
ruta_carpeta = r"H:\UNMSM\Cycle_IX\Thesis_I\Dataset\caidas\data\images\train"

# Extensiones válidas
extensiones_validas = {'.jpg', '.jpeg', '.png'}

# Recorrer todos los archivos en la carpeta
for archivo in os.listdir(ruta_carpeta):
    ruta_archivo = os.path.join(ruta_carpeta, archivo)

    # Verificar que sea un archivo (no carpeta)
    if os.path.isfile(ruta_archivo):
        _, extension = os.path.splitext(archivo)
        extension = extension.lower()

        # Eliminar si no tiene una extensión válida
        if extension not in extensiones_validas:
            print(f"[EXTENSIÓN INVÁLIDA] Eliminando: {archivo}")
            os.remove(ruta_archivo)
            continue

        # Verificar si realmente es una imagen usando PIL
        try:
            with Image.open(ruta_archivo) as img:
                img.verify()  # Solo verifica si se puede abrir
        except (UnidentifiedImageError, OSError):
            print(f"[IMAGEN INVÁLIDA] Eliminando: {archivo}")
            os.remove(ruta_archivo)

print("Proceso completado.")
