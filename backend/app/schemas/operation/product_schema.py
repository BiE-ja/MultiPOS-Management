from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Pour le produit
class ProductBase(BaseModel):
    name: str
    description : Optional[str]= None
    category_id : Optional[int] = None
    price : float
    init_stock: float

class ProductCreate(ProductBase):
    price : float
    init_sotck : float

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category_id : Optional[int]

class ProductRead(ProductBase):
    id: int
    price:float
    actual_stock : int

    class Config:
        orm_mode = True

# Pour la catégorie de produit
class ProductCategoryBase(BaseModel):
    id: int
    cat_name: str

    class Config:
        orm_mode = True


# Pour l'historique de prix
class PriceHistoryBase(BaseModel):
    produit_id: int
    type:str
    price:float

class PriceHistoryCreate(ProductBase):
    pass

class PriceHistoryRead(ProductBase):
    id: int
    product_id : int
    price : float
    date: datetime
    
    class Config:
        orm_mode = True