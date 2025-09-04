from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StockMovementBase(BaseModel):
    area_id: int
    product_id: int
    direction: str
    operation: str
    dateof: datetime | None
    quantity: Optional[int] = None
    comment: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    created_by: int
    initiated_by: int
    operation_id: int  # Represent a sale_id or a purchase_id who enclenched the movement in stock


class StockMovementUpdate(BaseModel):
    area_id: int | None
    product_id: int | None
    direction: str | None
    operation: str | None
    quantity: int | None
    create_at: datetime | None
    created_by: int | None
    dateOf: datetime | None
    comment: str | None
    initiated_by: int | None
    updated_by: int | None
    updated_at: datetime | None
    sale_id: int | None
    purchase_id: int | None


class StockMovementRead(StockMovementBase):
    id: int
    dateOf: datetime

    class config:
        orm_mode = True


class StockMovementReadUpdate(StockMovementBase):
    id: int
    updated_by: int
    updated_at: datetime
    reason: str

    class config:
        orm_mode = True


class InvotoryBase(BaseModel):
    area_id: int
    product_id: int
    dateof: datetime
    theoritical_quantity: float
    counted_quantity: float
    investigation_notes: str | None = None
    validated_quantity: float | None = None
    investigated_by_id: int | None = None


class InvotoryCreate(InvotoryBase):
    pass


class InvotoryUpdate(BaseModel):
    area_id: int | None = None
    product_id: int | None = None
    dateof: datetime | None = None
    theoritical_quantity: float | None = None
    counted_quantity: float | None = None
    investigation_notes: str | None = None
    validated_quantity: float | None = None
    investigated_by_id: int | None = None


class InvotoryRead(InvotoryBase):
    id: int

    model_config = {"from_attributes": True}
