""" -*- coding: utf-8 -*- """
# modelos entrenados de YOLO
# Este archivo contiene la carga de los modelos YOLO entrenados.
from ultralytics import YOLO

# Cargar solo el modelo que se desea probar actualmente
model_suspicious = YOLO("app/models/yolo_suspicious.pt")

# Modelos listos para activarse cuando estén validados
# model_people = YOLO("app/models/yolo_people.pt")
# model_falls = YOLO("app/models/yolo_falls.pt")
# model_fire = YOLO("app/models/yolo_fire.pt")
