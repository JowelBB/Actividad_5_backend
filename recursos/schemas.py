from pydantic import BaseModel, EmailStr
from typing import Optional

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str


# Para la respuesta del token
class Token(BaseModel):
    access_token: str
    token_type: str

# Para los datos dentro del token (payload)
class TokenData(BaseModel):
    username: Optional[str] = None


# Para las credenciales de inicio de sesión
class UserLogin(BaseModel):
    username: str
    password: str

# Modelo base para el usuario
class UserInDB(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    active: Optional[bool] = True

    class Config:
        from_attributes = True # Esto es 'orm_mode = True' para Pydantic v1.x

