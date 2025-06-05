from fastapi import FastAPI, Depends, HTTPException, Body, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta 

from db_config import SessionLocal, engine
from models import Base, Products, Users 
from recursos.schemas import CategoryCreate, CategoryUpdate, Token, UserLogin
from recursos.crud_productos import create_product, update_product, get_all_products, get_product, delete_product
from recursos.crud_categorias import create_category, update_category, get_all_categories, get_category, delete_category
from recursos.crud_usuarios import create_user, update_user, get_all_users, get_user

# Importa las funciones de autenticación
from recursos.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all request from any source
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods HTTP (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Allow all headers
)

#Create tables in the databse
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutes for products
@app.post("/productos/")
async def post_item_endpoint(name: str = Body(...), description: str = Body(...), price: int = Body(...), categoria_id: int = Body(...) , db: Session = Depends(get_db)):
    return create_product(db, name, description, price, categoria_id)

@app.get("/productos/")
async def get_all_items_endpoint(db: Session = Depends(get_db)):
    products = get_all_products(db)
    return products

@app.get("/productos/{product_id}")
async def get_item_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/productos/{product_id}")
async def update_item_endpoint(product_id: int, name: str = Body(...), description: str = Body(...), price: int = Body(...), categoria_id: int = Body(...), db: Session = Depends(get_db)):
    print(f"Intentando actualizar",product_id, name, description, price, categoria_id)
    updated_product = update_product(db, product_id, name, description, price, categoria_id)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/productos/{product_id}")
async def delete_item_endpoint(product_id: int, db: Session = Depends(get_db)):
    if delete_product(db, product_id):
        return {"detail": "Deleted product"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# Rutes for Categories
@app.post("/categorias/")
async def post_category_endpoint(category_data: CategoryCreate = Body(...), db: Session = Depends(get_db)):
    return create_category(db, category_data.name)

@app.get("/categorias/")
async def get_all_categories_endpoint(db: Session = Depends(get_db)):
    categories = get_all_categories(db)
    return categories

@app.get("/categorias/{category_id}")
async def get_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.put("/categorias/{category_id}")
async def update_category_endpoint(category_id: int, category_data: CategoryUpdate = Body(...), db: Session = Depends(get_db)):
    updated_category = update_category(db, category_id, category_data.name)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@app.delete("/categorias/{category_id}")
async def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    if delete_category(db, category_id):
        return {"detail": "Deleted category"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    

# --Rutes for users--
# rutes for signup
@app.post("/usuarios/")
async def post_user_endpint(full_name: str = Body(...), email: str = Body(...), username: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    return create_user(db, full_name, email, username, password)

@app.get("/usuarios/")
async def get_all_users_endpoint(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@app.get("/usuarios/{user_id}")
async def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/usuarios/{user_id}")
async def update_user_endpoint(user_id: int, full_name: str = Body(...), email: str = Body(...), username: str = Body(...), password: str = Body(...), status: int = Body(...), db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, full_name, email, username, password, status)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Endpoint de Inicio de Sesión (generará el JWT)
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # Espera username y password en formato x-www-form-urlencoded
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta protegida (solo accesible con un token JWT válido)
@app.get("/users/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email, "full_name": current_user.full_name}