from sqlalchemy.orm import Session

from backend.app.models.area import Area
from backend.app.models.product import Product, ProductCategory
from backend.app.schemas.area_schema import AreaCreate, AreaUpdate

def create_area(db:Session, area: AreaCreate):
    db_area= Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

def get_Area(db:Session, area_id:int):
    return db.query(Area).filter(Area.id==area_id).first()

def update_Area(db:Session, area_id:int, area_update: AreaUpdate):
    db_area = db.query(Area).filter(Area.id==area_id).first()
    if db_area:
        for var, value in area_update.model_dump(exclude_unset=True).items():
            setattr(db_area, var, value)
        db.commit()
        db.refresh(db_area)
    return db_area

def delete_area(db:Session, area_id:int):
    db_area = get_Area(db=db, area_id= area_id)
    if db_area :
        db.delete(db_area)
        db.commit()
    return None

#obtain list of area managed by a user
def list_managed_area(db:Session, owner_id:int, skip:int=0, limit:int=10):
    return (
        db.query(Area)
        .filter(Area.owner==owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
# return a list of all product for area passed in parameter
def get_area_products(db: Session, area_id:int, skip:int=0, limit:int=10):
    return (
        db.query(Product)
        .filter(Product.area_id == area_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

# return a list of all product categories for area passed in parameter
def get_area_product_categories(db: Session, area_id : int, skip: int=0, limit: int = 10):
    return (
        db.query(ProductCategory)
        .filter(Product.area_id == area_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

#def area_inventory (db : Session, area_id:int, skip:int=0, limit:int=10):
    