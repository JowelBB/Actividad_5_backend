from passlib.context import CryptContext

# Configuration for password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Encrypt the password before saving
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plaintext password matches a hashed one"""
    return pwd_context.verify(plain_password, hashed_password)

