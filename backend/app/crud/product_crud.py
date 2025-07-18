from sqlalchemy.orm import Session
from backend.app.models.product import Product, ProductCategory
from backend.app.schemas.product_schema import ProductCategoryBase, ProductCreate, ProductUpdate


def create_product(db:Session, product: ProductCreate):
    db_prod= Product(**product.model_dump())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod
    
def get_product(db:Session, product_id:int):
    return db.query(Product).filter(Product.id==product_id).first()

def update_product(db:Session, product_id:int, produit_update: ProductUpdate):
    db_prod = db.query(Product).filter(Product.id==product_id).first()
    if db_prod:
        for var, value in produit_update.model_dump(exclude_unset=True).items():
            setattr(db_prod, var, value)
        db.commit()
        db.refresh(db_prod)
    return db_prod

def list_products(db:Session, skip:int=0, limit:int=10):
    return db.query(Product).offset(skip).limit(limit).all()

def create_category(db:Session, category:ProductCategoryBase):
    db_prod = ProductCategory(**ProductCategory.model_dump())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def get_productCategory(db:Session, category_id:int):
    return db.query(ProductCategory).filter(ProductCategory.id==category_id).first()

def update_productCategory(db: Session, category_id:int, category_update : ProductCategoryBase):
    db_prod = db.query(ProductCategory).filter(ProductCategory.id==category_id).first()
    if db_prod:
        for var, value in category_update.model_dump(exclude_unset=True).items():
            setattr(db_prod, var, value)
        db.commit()
        db.refresh(db_prod)
    return db_prod

def list_category(db:Session, skip:int=0, limit:int=10):
    return db.query(ProductCategory).offset(skip).limit(limit).all()

