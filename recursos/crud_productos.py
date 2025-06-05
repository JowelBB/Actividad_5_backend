from sqlalchemy.orm import Session
from models import Products

def get_all_products(db: Session):
    return db.query(Products).all()

def get_product(db: Session, product_id: int):
    return db.query(Products).filter(Products.id == product_id).first()

def create_product(db: Session, name: str, description: str, price: int, categoria_id: int):
    db_product = Products(nombre=name, descripcion=description, precio=price, categoria_id=categoria_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, name: str = None, description: str = None, price: int = None, categoria_id: int = None):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if db_product:
        if name is not None:
            db_product.nombre = name
        if description is not None:
            db_product.descripcion = description
        if price is not None:
            db_product.precio = price
        if categoria_id is not None:
            db_product.categoria_id = categoria_id
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if db_product:
        db.delete(db_product)
        try:
            db.commit()
            return True
        except Exception as e:
            print(f"Error durante el commit de eliminación del producto: {e}")
            db.rollback()  # to roll back in case of error
            return False
    else:
        print("Producto no encontrado")
        return False