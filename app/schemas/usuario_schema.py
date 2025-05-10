from pydantic import BaseModel, EmailStr

# Esquema de entrada (para crear usuario)
class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    rol: str

# Esquema de respuesta (lo que regresa el servidor)
class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    rol: str

    class Config:
        orm_mode = True  # Permite que Pydantic trabaje con objetos ORM de SQLAlchemy
