from sqlalchemy.orm import Session
from models import Categories

def get_all_categories(db: Session):
    return db.query(Categories).all()

def get_category(db: Session, category_id: int):
    return db.query(Categories).filter(Categories.id == category_id).first()

def create_category(db: Session, name: str):
    db_category = Categories(nombre=name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return(db_category)

def update_category(db: Session, category_id: int = None, name: str = None):
    db_category = db.query(Categories).filter(Categories.id == category_id).first()
    if db_category:
        if name is not None:
            db_category.nombre = name
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(Categories).filter(Categories.id == category_id).first()
    if db_category:
        db.delete(db_category)
        try:
            db.commit()
            return True
        except Exception as e:
            print(f"Error durante el commit: {e}")
            db.rollback()  # to roll back in case of error
            return False
    else:
        print("Categoría no encontrada")
        return False
    