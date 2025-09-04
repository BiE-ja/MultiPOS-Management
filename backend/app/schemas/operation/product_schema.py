from pydantic import BaseModel
from datetime import datetime

from app.models.operation.product import ProductCreationState
from app.models.operation.product import PriceType

# Pour le produit
class ProductBase(BaseModel):
    reference : str
    name: str
    description : str | None
    category_name : str | None
    area_id : int

class ProductManagementBase(ProductBase):
    price: float
    purchase_price : float | None
    init_stock : float | None
    actual_stock : float | None
    # area_id : int | None  # area_id is already in ProductBase
class ProductCreate(ProductManagementBase):
    pass

class ProductUpdate(BaseModel):
    reference: str | None = None
    name: str | None = None
    description: str | None = None
    category_name : str | None = None
    area_id : int | None = None
    state : ProductCreationState | None = None
    
    sale_price: float | None = None
    purchase_price : float | None = None 
    init_stock : float | None = None
    actual_stock :float | None = None
    comment: str | None = None
    updated_by_id: int | None = None  # Assuming this is the ID of the user making the update 

class ProductRead(ProductManagementBase):
    id: int
    state : ProductCreationState

    class Config:
        orm_mode = True

class ProductDashbordRead(ProductManagementBase):
    id: int
    state : ProductCreationState
    incoming_quantity: float | None = None
    outgoing_quantity: float | None = None

    class Config:
        orm_mode = True
        
# Pour la catégorie de produit
class ProductCategoryBase(BaseModel):
    cat_name: str
    area_id : int

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryUpdate(BaseModel):
    area_id : int | None
    cat_name : str | None

class ProductCategoryRead(ProductCategoryBase):
    id : int
    class Config:
        orm_mode = True


# Pour l'historique de prix
class PriceHistoryBase(BaseModel):
    product_id: int
    type: PriceType
    value:float

class PriceHistoryCreate(PriceHistoryBase):
    pass

class PriceHistoryRead(PriceHistoryBase):
    id: int
    date: datetime
    
    class Config:
        orm_mode = True