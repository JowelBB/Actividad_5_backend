# recursos/auth.py
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db_config import SessionLocal
from models import Users
from recursos.schemas import TokenData
from recursos.password_hash import get_password_hash, verify_password


# --- Configuración de Seguridad ---
# Puedes generarla con: openssl rand -hex 32
SECRET_KEY = "warrwaar"
ALGORITHM = "HS256" # Algoritmo de hashing para JWT

# Tiempo de expiración del token de acceso en minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

# Esquema de seguridad OAuth2 para el flujo de contraseña
# El tokenUrl apunta a la ruta donde el cliente obtendrá el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Funciones para JWT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un nuevo token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # Valor por defecto
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Función para Autenticar Usuario (basada en tu crud_usuarios) ---
def get_user_by_username(db: Session, username: str):
    """Busca un usuario por su nombre de usuario."""
    return db.query(Users).filter(Users.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    """Autentica un usuario con su nombre de usuario y contraseña."""
    user = get_user_by_username(db, username)
    if not user:
        return False # Usuario no encontrado
    if not verify_password(password, user.password_hash):
        return False # Contraseña incorrecta
    # Puedes añadir aquí una verificación para active si lo tienes
    # if not user.active:
    #     return False
    return user

# --- Dependencia para Obtener el Usuario Actual (Protección de Rutas) ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Decodifica el token JWT y obtiene el usuario autenticado.
    Esta dependencia se usa para proteger rutas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # 'sub' es el sujeto (subject) del token
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, token_data.username) # Obtener el usuario de la DB
    if user is None:
        raise credentials_exception
    return user

