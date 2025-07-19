from datetime import datetime
from pydantic import BaseModel


class PaymentBase(BaseModel):
    ref : str | None
    method : str
    cash_transact_id : int | None
    dateof : datetime

class PaymentCreate(PaymentBase):
    amount : float

class PaymentUpdate(BaseModel):
    ref : str | None
    method : str | None
    sale_id : int | None
    cash_transact_id : int | None
    dateof : datetime | None
    amount : float | None

class PaymentRead(PaymentBase):
    id : int
    class Config:
        orm_mode = True

class PaymentCashRead(PaymentBase):
    id : int
    sale_id : int
    class Config:
        orm_mode = True

class TransactionCashBase(BaseModel):
    direction : str
    purpose : str
    status : str

class TransactionCashCreate(TransactionCashBase):
    pass

class TransactionCashUpdate(BaseModel):
    direction: str | None
    purpose : str | None
    status : str | None
    user_id : int | None
    cancellation : str | None
    cancel_date : datetime | None
    canceled_by : int | None
    register: int | None
    payment_ref : int | None
    dateof : datetime | None

class TransactionCashRead(TransactionCashBase):
    id : int
    is_valide : str
    amount : float
    class Config:
        orm_mode = True

class TransactionCashLineBase(BaseModel):
    denomination : int | None
    transac : int | None
    quantity: int

class TransactionCashLineCreate(TransactionCashBase):
    pass

class TransactionCashLineUpdate(BaseModel):
    denomination : int | None
    transac : int | None
    quantity : int | None

class TransactionCashLineRead(TransactionCashLineBase):
    id : int
    value : float
    class Config:
        orm_mode = True

class DenominationBase(BaseModel):
    name : str
    value : int
    currency : str

class DenominationUpdate(BaseModel):
    name : str| None
    value : int | None
    currency : str | None

class DenominationCreate(DenominationBase):
    pass

class DenominationRead(DenominationBase):
    id: int
    class config:
        orm_mode = True


