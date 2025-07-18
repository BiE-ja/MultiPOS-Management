from typing import Optional
from pydantic import BaseModel


class AreaBase(BaseModel):
    name : str
    location : Optional[str]= None
    owner_id : Optional[int] = None

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):
    name : Optional[str]
    location: Optional[str]
    owner_id : Optional[int]

class AreaRead(AreaBase):
    id : int
    class config:
        orm_mode = True