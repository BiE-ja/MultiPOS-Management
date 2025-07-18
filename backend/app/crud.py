from sqlalchemy.orm import Session
from app import schemas
from app.models import models

def create_produit(db: Session, product: schemas.ProductCreate):
    db_obj = models.Product(**product.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_produits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.ClientCreate):
    db_obj = models.Customer(**customer.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

def create_vente(db: Session, vente: schemas.VenteCreate):
    db_obj = models.Vente(**vente.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_ventes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vente).offset(skip).limit(limit).all()
