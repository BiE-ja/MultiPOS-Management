from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockMovementBase(BaseModel):
    product_id : int
    movementType_id : int
    quantity : Optional[int] = None
    comment : Optional[str] = None

class StockMovementRead(StockMovementBase):
    id :int
    move_date: datetime
