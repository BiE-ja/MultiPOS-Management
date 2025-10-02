import uuid
from pydantic import BaseModel
from datetime import datetime

from app.dto.models.models import ProductCreationState, PriceType


# Pour le produit
class ProductBase(BaseModel):
    reference: str
    name: str
    description: str | None
    category_name: str | None
    area_id: uuid.UUID


class ProductManagementBase(ProductBase):
    price: float
    purchase_price: float | None
    init_stock: float | None
    actual_stock: float | None
    # area_id : int | None  # area_id is already in ProductBase


class ProductCreate(ProductManagementBase):
    pass


class ProductUpdate(BaseModel):
    reference: str | None = None
    name: str | None = None
    description: str | None = None
    category_name: str | None = None
    area_id: uuid.UUID | None = None
    state: ProductCreationState | None = None

    sale_price: float | None = None
    purchase_price: float | None = None
    init_stock: float | None = None
    actual_stock: float | None = None
    comment: str | None = None
    updated_by_id: uuid.UUID | None = None  # Assuming this is the ID of the user making the update


class ProductRead(ProductManagementBase):
    id: uuid.UUID
    state: ProductCreationState

    model_config = {"from_attributes": True}


class ProductDashbordRead(ProductManagementBase):
    id: uuid.UUID
    state: ProductCreationState
    incoming_quantity: float | None = None
    outgoing_quantity: float | None = None

    model_config = {"from_attributes": True}


# Pour la catégorie de produit
class ProductCategoryBase(BaseModel):
    cat_name: str
    area_id: uuid.UUID


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(BaseModel):
    area_id: uuid.UUID | None
    cat_name: str | None


class ProductCategoryRead(ProductCategoryBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}


# Pour l'historique de prix
class PriceHistoryBase(BaseModel):
    product_id: uuid.UUID
    type: PriceType
    value: float


class PriceHistoryCreate(PriceHistoryBase):
    pass


class PriceHistoryRead(PriceHistoryBase):
    id: uuid.UUID
    date: datetime

    model_config = {"from_attributes": True}


class LotCreate(BaseModel):
    product_id: uuid.UUID
    quantity: float
    perimed_at: datetime | None = None  # Optional expiration date
    purchase_price: float | None = None  # Optional purchase price


class LotRead(LotCreate):
    id: uuid.UUID

    model_config = {"from_attributes": True}
