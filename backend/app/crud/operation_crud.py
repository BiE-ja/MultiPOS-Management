from sqlalchemy.orm import Session

from backend.app.models.operation.stock import Product, ProductCategory

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