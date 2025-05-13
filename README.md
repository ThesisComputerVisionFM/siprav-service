# siprav-client

```
`+
backend/
├── app/
│   ├── main.py                # Punto de entrada (FastAPI + WebSocket)
│   ├── database/              # Conexión SQLite y creación de tabla
|       ├── database.py
│   ├── models/                # Modelos YOLOv8x cargados
│   │   ├── yolo_people.pt
│   │   ├── yolo_falls.pt
│   │   ├── yolo_fire.pt
│   │   └── yolo_suspicious.pt
│   ├── yolo_engine.py         # Código que maneja la inferencia con YOLO
|   ├── schemas/
│   |   ├── alert_schema.py            # Pydantic models para la validación de datos
│   |   ├── camera_schema.py            # Pydantic models para la validación de datos
│   ├── services/                #
│   │   ├── camera_streamer.py
│   └── routers/
│       ├── cameras.py         # Endpoints REST para CRUD de cámaras
│       ├── alert.py         # Endpoints REST para CRUD de alertas
│       └── stream.py          # WebSocket para enviar/recibir detecciones
└── requirements.txt

```

`uvicorn app.main:app --reload`

`GET http://localhost:8000/cameras/mock`
