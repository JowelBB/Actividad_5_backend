from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#   Datos para conexion a la bd, credneciales y config
DATABASE_URL = "mysql+pymysql://sql10782942:U1u6e68AdL@sql10.freesqldatabase.com:3306/sql10782942"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()