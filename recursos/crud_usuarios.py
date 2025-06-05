from sqlalchemy.orm import Session
from models import Users
from fastapi import HTTPException, status
from recursos.password_hash import get_password_hash

def get_all_users(db: Session):
    return db.query(Users).all()

def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()

def create_user(db: Session, full_name: str, email: str, username: str, password: str):
    db_user_email = get_user_by_email(db, email)
    if db_user_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El correo electrónico ya está registrado.")
    db_user_username = get_user_by_username(db, username)
    if db_user_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de usuario ya está en uso.")

    # Hash the password before storing it
    hashed_password = get_password_hash(password)

    # Create the user object and save it in the database
    db_user = Users(full_name=full_name, email=email, username=username, password_hash=hashed_password, active=1)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, full_name: str = None, email: str = None, username: str = None, password: str = None, active: int = None):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user:
        if full_name is not None:
            db_user.full_name = full_name
        if email is not None:
            db_user.email = email
        if username is not None:
            db_user.username = username
        if password is not None:
            db_user.password_hash = password
        if active is not None:
            db_user.active = active
    db.commit()
    db.refresh(db_user)
    return db_user
        