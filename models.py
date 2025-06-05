from sqlalchemy import Column, Integer, String
from db_config import Base

class Products(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), index=True)
    descripcion = Column(String(255), index=True)
    precio = Column(Integer)
    categoria_id = Column(Integer)

class Categories(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), index=True)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(55), index=True)
    email = Column(String(55), index=True)
    username = Column(String(55), index=True)
    password_hash = Column(String(255))
    active = Column(Integer)

class Tokens(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    token = Column(String(255))
    active = Column(Integer)


