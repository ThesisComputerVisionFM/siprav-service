import cv2
import time

# OPCIONES de conexión (elige la adecuada)
# HTTP snapshot (solo si la cámara envía una imagen continua como MJPEG)
http_url = "http://192.168.90.107:8080/video"  # o /shot.jpg
# RTSP (comentar si no lo usas)
# rtsp_url = "rtsp://192.168.90.107:554/h264_ulaw.sdp"

# Usa la URL correcta para tu cámara
camera_url = http_url  # o rtsp_url

# Iniciar captura
cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("❌ No se pudo conectar a la cámara.")
    exit()

print("✅ Conectado. Mostrando video por 3 minutos...")

# Tiempo límite: 3 minutos
start_time = time.time()
duration = 3 * 60  # 3 minutos en segundos

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo leer el fotograma.")
        break

    cv2.imshow("Stream en Vivo - Presiona ESC para salir", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # tecla ESC
        break

    if time.time() - start_time > duration:
        print("⏱️ Tiempo completado.")
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
