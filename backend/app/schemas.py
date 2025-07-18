from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    nom: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    nom: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: int

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    date: datetime
    class Config:
        orm_mode = True
class SupplierBase (BaseModel) :
    nom :str
    email : str

class SupplierCreate(SupplierBase) :
    pass

class Supplier(SupplierBase) :
    id : int
    class Config :
        orm_mode = True