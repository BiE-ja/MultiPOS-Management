import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StockMovementBase(BaseModel):
    area_id: uuid.UUID
    product_id: uuid.UUID
    product_lot_id: Optional[uuid.UUID] = None  # optional
    direction: str
    operation: str
    dateof: datetime | None
    quantity: Optional[int] = None
    comment: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    created_by: uuid.UUID
    initiated_by: uuid.UUID
    operation_id: uuid.UUID  # Represent a sale_id or a purchase_id who enclenched the movement in stock


class StockMovementUpdate(BaseModel):
    area_id: uuid.UUID | None
    product_id: uuid.UUID | None
    product_lot_id: Optional[uuid.UUID] = None  # optional
    direction: str | None
    operation: str | None
    quantity: int | None
    create_at: datetime | None
    created_by: uuid.UUID | None
    dateOf: datetime | None
    comment: str | None
    initiated_by: uuid.UUID | None
    updated_by: uuid.UUID | None
    updated_at: datetime | None
    sale_id: uuid.UUID | None
    purchase_id: uuid.UUID | None


class StockMovementRead(StockMovementBase):
    id: uuid.UUID
    dateOf: datetime

    model_config = {"from_attributes": True}


class StockMovementReadUpdate(StockMovementBase):
    id: uuid.UUID
    updated_by: int
    updated_at: datetime
    reason: str

    model_config = {"from_attributes": True}


class InvotoryBase(BaseModel):
    area_id: uuid.UUID
    product_id: uuid.UUID
    dateof: datetime
    theoritical_quantity: float
    counted_quantity: float
    investigation_notes: str | None = None
    validated_quantity: float | None = None
    investigated_by_id: uuid.UUID | None = None


class InvotoryCreate(InvotoryBase):
    pass


class InvotoryUpdate(BaseModel):
    area_id: uuid.UUID | None = None
    product_id: uuid.UUID | None = None
    dateof: datetime | None = None
    theoritical_quantity: float | None = None
    counted_quantity: float | None = None
    investigation_notes: str | None = None
    validated_quantity: float | None = None
    investigated_by_id: uuid.UUID | None = None


class InvotoryRead(InvotoryBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}
