from pydantic import BaseModel, EmailStr
from typing import Optional

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str


# For the token response
class Token(BaseModel):
    access_token: str
    token_type: str

# For data within the token (payload)
class TokenData(BaseModel):
    username: Optional[str] = None


# For login credentials
class UserLogin(BaseModel):
    username: str
    password: str

# Base model for the user
class UserInDB(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    active: Optional[bool] = True

    class Config:
        from_attributes = True # Esto es 'orm_mode = True' para Pydantic v1.x

