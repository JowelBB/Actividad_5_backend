from sqlalchemy.orm import Session
from models import Users
from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError
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
    if not email or len(email) > 55:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email es requerido y no debe exceder los 55 caracteres.")
    if not username or len(username) < 3 or len(username) > 55:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario es requerido y debe tener entre 3 y 55 caracteres.")
    if full_name and len(full_name) > 55:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre completo no debe exceder los 55 caracteres.")
    if not password:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no puede estar vacía.")
    try:
        # validate_email returns an object, .email gives us the normalized address
        # check_deliverability=False to avoid making DNS queries
        validated_email_address = validate_email(email, check_deliverability=False).email
    except EmailNotValidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El formato del correo electrónico '{email}' no es válido: {e}")

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
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    if email is not None:
        if not email.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email no puede estar vacío.")
        if len(email) > 55:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email no debe exceder los 55 caracteres.")
        try:
            # Validate and normalize the email
            validated_email_address = validate_email(email, check_deliverability=False).email
        except EmailNotValidError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El formato del correo electrónico '{email}' no es válido: {e}")

        # validate that the email is not duplicated
        if validated_email_address != db_user.email:
            db_user_email_check = get_user_by_email(db, validated_email_address)
            if db_user_email_check:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nuevo correo electrónico ya está registrado por otro usuario.")  
        db_user.email = validated_email_address

    # Validation and update of Username
    if username is not None:
        if not username.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario no puede estar vacío.")
        if len(username) < 3 or len(username) > 55:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario debe tener entre 3 y 55 caracteres.")
        # Check if the user is duplicated
        if username != db_user.username:
            db_user_username_check = get_user_by_username(db, username)
            if db_user_username_check:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nuevo nombre de usuario ya está en uso por otro usuario.") 
        db_user.username = username

    # Validation and update of Full Name
    if full_name is not None:
        if full_name and len(full_name) > 55:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre completo no debe exceder los 55 caracteres.")
        db_user.full_name = full_name

    # Validation and update of Password
    if password is not None:
        if not password.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no puede estar vacía.")
        db_user.password_hash = get_password_hash(password) # Hashear the new password

    # Validation and update of Active status
    if active is not None:
        if active not in [0, 1]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El estado 'activo' debe ser 0 o 1.")
        db_user.active = active
    db.commit()
    db.refresh(db_user)
    return db_user