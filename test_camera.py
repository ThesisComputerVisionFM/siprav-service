import cv2
import time

# --- CONFIGURACIÓN ---
# Elige el tipo de stream y la URL correspondiente
STREAM_TYPE = "HTTP"  # Opciones: "HTTP", "RTSP", "FILE"
# STREAM_TYPE = "RTSP"
# STREAM_TYPE = "FILE" # Para probar con un archivo de video local

# URLs (ajusta según tu configuración)
HTTP_URL = "http://192.168.1.137:8080/video"  # Puede ser la URL base del stream MJPEG o una URL a /shot.jpg, /video, etc.
RTSP_URL = "rtsp://user:password@192.168.1.100:554/stream1" # Ejemplo: rtsp://user:pass@ip:port/path
VIDEO_FILE_PATH = "ruta/a/tu/video.mp4" # Ejemplo: "C:/videos/test.mp4"

# Duración de la prueba en segundos (0 para indefinido hasta ESC)
TEST_DURATION_SECONDS = 3 * 60  # 3 minutos

# Backend de OpenCV (opcional, prueba si tienes problemas)
# Puede ser cv2.CAP_FFMPEG, cv2.CAP_GSTREAMER, etc. Déjalo como None para automático.
OPENCV_BACKEND = None # O cv2.CAP_FFMPEG

# --- LÓGICA DE PRUEBA ---
camera_url = None
if STREAM_TYPE == "HTTP":
    camera_url = HTTP_URL
elif STREAM_TYPE == "RTSP":
    camera_url = RTSP_URL
elif STREAM_TYPE == "FILE":
    camera_url = VIDEO_FILE_PATH
else:
    print(f"❌ Tipo de stream no válido: {STREAM_TYPE}")
    exit()

print(f"ℹ️ Intentando conectar a: {camera_url} (Tipo: {STREAM_TYPE})")

# Iniciar captura
if OPENCV_BACKEND is not None:
    cap = cv2.VideoCapture(camera_url, OPENCV_BACKEND)
else:
    cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("❌ No se pudo conectar a la fuente de video.")
    print("   Posibles causas:")
    print("   - URL incorrecta o la cámara/archivo no está accesible.")
    print("   - Firewall bloqueando la conexión.")
    print("   - Codecs necesarios no disponibles (para RTSP/archivos).")
    print("   - Si es HTTP, asegúrate que sea un stream MJPEG o una URL de snapshot que se actualice.")
    exit()

print("✅ Conectado exitosamente a la fuente de video.")

# Obtener información del stream (si es posible)
try:
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"   Resolución: {width}x{height}")
    if fps > 0:
        print(f"   FPS (reportado): {fps:.2f}")
    else:
        print(f"   FPS (reportado): N/A (común para algunos streams HTTP o si no se puede determinar)")
except Exception as e:
    print(f"   ⚠️ No se pudo obtener toda la información del stream: {e}")


if TEST_DURATION_SECONDS > 0:
    print(f"📺 Mostrando video por {TEST_DURATION_SECONDS // 60} minuto(s) y {TEST_DURATION_SECONDS % 60} segundo(s)...")
else:
    print(f"📺 Mostrando video indefinidamente...")
print("   Presiona 'ESC' para salir antes.")


start_time = time.time()
frame_count = 0
display_fps_interval = 1 # segundos
last_fps_time = time.time()
frames_since_last_fps_calc = 0

window_name = f"Stream {STREAM_TYPE} - {camera_url} - ESC para salir"

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo leer el fotograma. El stream puede haber terminado o se perdió la conexión.")
        # Si es un archivo de video, esto es normal al final
        if STREAM_TYPE == "FILE":
            print("   (Fin del archivo de video)")
        break

    frame_count += 1
    frames_since_last_fps_calc +=1

    # Calcular y mostrar FPS de visualización
    current_time = time.time()
    if (current_time - last_fps_time) >= display_fps_interval:
        actual_display_fps = frames_since_last_fps_calc / (current_time - last_fps_time)
        # print(f"Display FPS: {actual_display_fps:.2f}") # Opcional: imprimir en consola
        cv2.putText(frame, f"Display FPS: {actual_display_fps:.2f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        last_fps_time = current_time
        frames_since_last_fps_calc = 0

    cv2.imshow(window_name, frame)

    key = cv2.waitKey(1) & 0xFF # El '1' es importante para que el video fluya
    if key == 27:  # tecla ESC
        print("🚪 Saliendo por petición del usuario (ESC).")
        break

    if TEST_DURATION_SECONDS > 0 and (time.time() - start_time > TEST_DURATION_SECONDS):
        print("⏱️ Tiempo de prueba completado.")
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
print(f"📹 Total de fotogramas leídos: {frame_count}")
print("✅ Prueba finalizada.")