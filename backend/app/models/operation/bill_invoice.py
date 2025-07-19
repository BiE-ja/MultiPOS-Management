from datetime import datetime, timezone
from enum import Enum as pyEnum
from typing import Any, List, Optional
from backend.app.database import Base
from sqlalchemy import Integer, ForeignKey, DateTime, Numeric, String, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates

from backend.app.models.deps import Area, User
from backend.app.models.finance.payment import Payment
from backend.app.models.operation.purchase import PurchaseRequest
from backend.app.models.operation.sale import Customer, Sale
from backend.app.models.operation.stock import Product

# Represents an invoice for purchases or sales
# It can be an incoming invoice (from a supplier) or an outgoing invoice (for a customer)
# It can be linked to a purchase request or a sale
class Invoice(Base):
    __tablename__="invoice"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    ref : Mapped[str | None]= mapped_column(String(50))
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"))
    dateof : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    created_by_id : Mapped[int]= mapped_column(ForeignKey("user.id"), nullable=False) 
    updated_by_id : Mapped[int | None]= mapped_column(ForeignKey("user.id"))
    updated_at : Mapped[datetime | None]= mapped_column(DateTime(timezone=True)) 
    type: Mapped["InvoiceType"]= mapped_column(sqlEnum("InvoiceType"), nullable=False)
    status: Mapped["Status"]= mapped_column(sqlEnum("Status"), nullable=False) 
    comments : Mapped[str | None]= mapped_column(String(255))
    amount_payed : Mapped[float | None]= mapped_column(Numeric(18,2), default=0.0)
    
    # optional FK (if invoice received)
    purchase_id: Mapped[int | None]= mapped_column(ForeignKey("purchaseRequest.id"))
    # optional FK (if invoice sent)
    sale_id: Mapped[int | None]= mapped_column(ForeignKey("sale.id"))

    payment_id : Mapped[int | None]= mapped_column(ForeignKey("payment.id"))

    supplier_id : Mapped[int | None]= mapped_column(ForeignKey("supplier.id")) 
    customer_id : Mapped[int | None]= mapped_column(ForeignKey("customer.id"))
    
    area : Mapped[Area] = relationship(back_populates="purchase")
    supplier : Mapped[Optional["Supplier"]] = relationship(back_populates="invoice", uselist=False)
    customer : Mapped[Optional["Customer"]] = relationship(back_populates="invoice", uselist=False)

    purchase: Mapped[Optional[PurchaseRequest]] = relationship(back_populates="invoice", uselist=False)
    sale : Mapped[Optional["Sale"]] = relationship(back_populates="invoice", uselist=False)
    # payment is optional, if invoice is not paid yet
    payment : Mapped[Optional[Payment]] = relationship(back_populates="invoice", lazy="joined")

    created_by: Mapped[User] = relationship(back_populates="invoice", foreign_keys="Invoice.created_by_id", lazy="joined", uselist=False)
    updated_by: Mapped[Optional[User]] = relationship(back_populates="invoice", foreign_keys="Invoice.updated_by_id", lazy="joined")

    details : Mapped[List["InvoiceDetailsLine"]] = relationship(back_populates="details", cascade="all, delete-orphan")
    # Optional FK stock movement, enclenched if purchase status is delivered

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details )

    @property
    def amount_to_pay(self):
        return sum(detail.amount_payable for detail in self.details)
    
    @validates("status", "amount_payed"):
    def validate_coherance(self, key, value)->Any: # type: ignore
        amount_payed = self.amount_payed
        if amount_payed == None :
            amount_payed = 0
        if key == "status":
            if value == Status.CLOSED and amount_payed < self.amount_to_pay:
                raise ValueError("Cannot close invoice, amount paid is less than amount to pay")
            if value == Status.REJECTED and amount_payed > 0:
                raise ValueError("Cannot reject invoice, amount paid is greater than zero")
        elif key == "amount_payed":
            if value < 0 or value > self.amount_to_pay:
                raise ValueError("Amount paid must be between 0 and total amount to pay")
        return value # type: ignore

class Status(pyEnum):
    OPENED = "open"
    CLOSED = "closed"
    PARTIAL = "partial"
    REJECTED = "rejected"

class InvoiceType(pyEnum):
    IN = "in"  # incoming invoice
    OUT = "out"  # outgoing invoice, for sale

class InvoiceDetailsLine(Base):
    __tablename__="invoice_details_line"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    invoice_id : Mapped[int]= mapped_column(ForeignKey("invoice.id"))
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"))
    quantity_requested : Mapped[int]= mapped_column(default= 0)
    quantity_real : Mapped[int | None]= mapped_column() # sended or receeived
    unitaryPrice : Mapped[float]= mapped_column(Numeric(18,2))  

    product : Mapped[Product]= relationship(back_populate ="invoice_detail", uselist=False) # one line : one product
    invoice : Mapped[Invoice]= relationship(back_populate ="invoice_detail", uselist=False)
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
    product : Mapped[List[Product]]= relationship(back_populates="supplier")
    invoice : Mapped[List[Invoice]]= relationship(back_populates="supplier")