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

# --- Security Settings ---
SECRET_KEY = "warrwaar"
ALGORITHM = "HS256" # Hashing algorithm for JWT

# Access token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

# OAuth2 security scheme for the password flow
# The tokenUrl points to the path where the client will obtain the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Functions for JWT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None): 
    "Create a new JWT access token."
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

# --- Function to Authenticate User (based on your crud_users) ---
def get_user_by_username(db: Session, username: str):
    """Search for a user by their username."""
    return db.query(Users).filter(Users.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    """Authenticates a user with their username and password."""
    user = get_user_by_username(db, username)
    if not user:
        return False # Usuario no encontrado
    if not verify_password(password, user.password_hash):
        return False # Contraseña incorrecta
    # Check if the user is active
    if not user.active:
        return False
    return user

# --- Dependency to Get Current User (Route Protection) ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Decodes the JWT token and obtains the authenticated user.
    This dependency is used to protect routes.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # 'sub' is the subject of the token
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, token_data.username) # Get the DB user
    if user is None:
        raise credentials_exception
    return user

