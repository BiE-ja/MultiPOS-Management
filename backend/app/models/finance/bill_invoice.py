from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, List, Optional, TYPE_CHECKING
from app.core.database import Base
from sqlalchemy import Integer, ForeignKey, DateTime, Numeric, String, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates

from .payment import TransactionState, TransactionType

if TYPE_CHECKING:
    from backend.app.models.finance.payment import Payment, TransactionState, TransactionType
    from backend.app.models.management.purchase import PurchaseRequest, Order
    from backend.app.models.management.sale import Customer
    from backend.app.models.management.unit import Area, Employee, User
    from backend.app.models.operation.product import Supplier_Product_List, Product
  
# Represents an invoice for purchases or sales
# It can be an incoming invoice (from a supplier) or an outgoing invoice (for a customer)
# It can be linked to a purchase request or a sale
class Invoice(Base):
    __tablename__="invoice"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    ref : Mapped[str | None]= mapped_column(String(50))
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"))
    dateof : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    initiated_by_id : Mapped[int]= mapped_column(ForeignKey("employee.id"), nullable=False)
    created_by_id : Mapped[int]= mapped_column(ForeignKey("user.id"), nullable=False) 
    updated_by_id : Mapped[int | None]= mapped_column(ForeignKey("user.id"))
    updated_at : Mapped[datetime | None]= mapped_column(DateTime(timezone=True)) 
    type: Mapped["TransactionType"]= mapped_column(sqlEnum(TransactionType), nullable=False)
    status: Mapped["TransactionState"]= mapped_column(sqlEnum(TransactionState), nullable=False) 
    comments : Mapped[str | None]= mapped_column(String(255))
    amount_payed : Mapped[float | None]= mapped_column(Numeric(18,2), default=0.0)
    
    # optional FK (if invoice received)
    purchase_id: Mapped[int | None]= mapped_column(ForeignKey("purchase_request.id"))
    # optional FK (if invoice sent)
    order_id: Mapped[int | None]= mapped_column(ForeignKey("order.id"))

    #payment_id : Mapped[int | None]= mapped_column(ForeignKey("payments.id"))

    supplier_id : Mapped[int | None]= mapped_column(ForeignKey("supplier.id")) 
    customer_id : Mapped[int | None]= mapped_column(ForeignKey("customer.id"))
    
    area : Mapped[Area] = relationship(back_populates="invoice")
    supplier : Mapped[Optional["Supplier"]] = relationship(back_populates="invoice", uselist=False)
    customer : Mapped[Optional["Customer"]] = relationship(back_populates="invoice", uselist=False)

    purchase: Mapped[Optional[PurchaseRequest]] = relationship(back_populates="invoice", uselist=False)
    order: Mapped[Optional[Order]] = relationship(back_populates="invoice", uselist=False)
    # payment is optional, if invoice is not paid yet
    payments : Mapped[Optional[Payment]] = relationship(back_populates="invoice", lazy="joined")

    initiated_by: Mapped[Employee] = relationship(back_populates="invoice_initiated", foreign_keys="Invoice.initiated_by_id", lazy="joined", uselist=False)
    created_by: Mapped[User] = relationship(back_populates="invoice_created", foreign_keys="Invoice.created_by_id", lazy="joined", uselist=False)
    updated_by: Mapped[Optional[User]] = relationship(back_populates="invoice_updated", foreign_keys="Invoice.updated_by_id", lazy="joined")

    details : Mapped[List["InvoiceDetailsLine"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")
    # Optional FK stock movement, enclenched if purchase status is delivered

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details )

    @property
    def amount_to_pay(self):
        return sum(detail.amount_payable for detail in self.details)
    
    @validates("status", "amount_payed")
    def validate_coherance(self, key, value)->Any: # type: ignore
        amount_payed = self.amount_payed
        if amount_payed == None :
            amount_payed = 0
        if key == "status":
            if value == TransactionState.CLOSED and amount_payed < self.amount_to_pay:
                raise ValueError("Cannot close invoice, amount paid is less than amount to pay")
            if value == TransactionState.REJECTED and amount_payed > 0:
                raise ValueError("Cannot reject invoice, amount paid is greater than zero")
        elif key == "amount_payed":
            if value < 0 or value > self.amount_to_pay:
                raise ValueError("Amount paid must be between 0 and total amount to pay")
        return value # type: ignore

class InvoiceDetailsLine(Base):
    __tablename__="invoice_details_line"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    invoice_id : Mapped[int]= mapped_column(ForeignKey("invoice.id"))
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"))
    quantity_requested : Mapped[int]= mapped_column(default= 0)
    quantity_real : Mapped[int | None]= mapped_column() # sended or receeived
    unitaryPrice : Mapped[float]= mapped_column(Numeric(18,2))  

    product : Mapped[Product]= relationship(back_populates ="invoice_detail", uselist=False) # one line : one product
    invoice : Mapped[Invoice]= relationship(back_populates ="details", uselist=False)
    @property
    def value(self):
        return (self.quantity_requested * self.unitaryPrice)
    @property
    def amount_payable(self):
        amount = 0
        if self.quantity_real != None : 
            amount = self.quantity_real * self.unitaryPrice
        return amount

    

class Supplier(Base):
    __tablename__= "supplier"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    name : Mapped[str]= mapped_column(String(50), unique= True)
    email : Mapped[str]= mapped_column(String(50), unique= True)
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"), nullable=False)

    area : Mapped[Area]= relationship(back_populates="supplier")
    product_list : Mapped[List[Supplier_Product_List]]= relationship(back_populates="supplier")
    invoice : Mapped[List[Invoice]]= relationship(back_populates="supplier")