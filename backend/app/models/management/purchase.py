from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from enum import Enum as pyEnum
from sqlalchemy import Integer, ForeignKey, DateTime, Numeric, String, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime, timezone


if TYPE_CHECKING:
    from backend.app.models.finance.bill_invoice import Invoice
    from backend.app.models.management.unit import Area, Employee, User
    from backend.app.models.operation.stock import Product, StockMovement
    from backend.app.models.management.sale import Customer
    
class Request_status(pyEnum):
    OPENED = "open"
    DELIVERED = "delivered"
    CLOSED = "closed"
    REJECTED = "rejected"
    
# Ici ça représente une demande d'approvisionnement enclenché par le magasinier ou son supérieur (manager, owner)
class PurchaseRequest(Base):
    __tablename__ = "purchase_request"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    reference : Mapped[str]= mapped_column(String(255), unique= True)
    dateof : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    initiated_by_id : Mapped[int]= mapped_column(ForeignKey("employee.id")) # employee who requested the purchase
    created_by_id : Mapped[int]= mapped_column(ForeignKey("user.id")) # the user who create the PR
    updated_by_id : Mapped[int | None]= mapped_column(ForeignKey("user.id")) # PR is closed if his rejected or transformed on bill invoice
    status: Mapped["Request_status"]= mapped_column(sqlEnum(Request_status), nullable=False)
    updated_at : Mapped[datetime | None]= mapped_column(DateTime(timezone=True))
    comments :Mapped[str | None ]= mapped_column(String(100)) 
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"))
    area : Mapped[Area] = relationship(back_populates="purchase")
    
    details : Mapped[List["PurchaseRequestDetailsLine"]] = relationship(back_populates="purchase", cascade="all, delete-orphan")
    
    initiated_by : Mapped[Employee] = relationship(back_populates="purchase_initiated", foreign_keys="PurchaseRequest.initiated_by_id", lazy="joined", uselist=False)
    created_by: Mapped[User] = relationship(back_populates="purchase_created", foreign_keys="PurchaseRequest.created_by_id", lazy="joined", uselist=False)
    updated_by: Mapped[Optional[User]] = relationship(back_populates="purchase_updated", foreign_keys="PurchaseRequest.updated_by_id", lazy="joined")
    invoice : Mapped[Optional[List[Invoice]]] = relationship(back_populates="purchase", lazy="joined")

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details )
    


class PurchaseRequestDetailsLine(Base):
    __tablename__="purchase_detail_line"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    purchase_id : Mapped[int]= mapped_column(ForeignKey("purchase_request.id"))
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"))
    quantity_requested : Mapped[int]= mapped_column(default= 0)
    quantity_accorded : Mapped[int | None]= mapped_column()
    unitaryPrice : Mapped[float]= mapped_column(Numeric(18,2))  
    #stock_movement_id : Mapped[int| None]= mapped_column(ForeignKey("stockMovement.id"))
    # stock movement enclenched when purchase status set to DELIVERD
    stock_movement : Mapped[Optional[StockMovement]]= relationship(back_populates ="purchase_details_line", uselist=False) 
    product : Mapped[Product]= relationship(back_populates ="purchase_detail", uselist=False) # one line : one product
    purchase : Mapped[PurchaseRequest]= relationship(back_populates ="details", uselist=False)
    @property
    def value(self):
        return (self.quantity_requested * self.unitaryPrice)
    

class Order(Base):
    __tablename__ = "order"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    reference : Mapped[str]= mapped_column(String(255), unique= True)
    dateof : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    initiated_by_id : Mapped[int]= mapped_column(ForeignKey("customer.id")) # customer who requested the order
    created_by_id : Mapped[int]= mapped_column(ForeignKey("user.id")) # the user who put the order in system
    updated_by_id : Mapped[int | None]= mapped_column(ForeignKey("user.id")) # order is closed if his rejected or transformed on bill invoice outgoing
    status: Mapped["Request_status"]= mapped_column(sqlEnum(Request_status), nullable=False)
    updated_at : Mapped[datetime | None]= mapped_column(DateTime(timezone=True))
    comments :Mapped[str | None ]= mapped_column(String(100)) 
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"))
    area : Mapped[Area] = relationship(back_populates="order")
    
    details : Mapped[List["OrderDetailsLine"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    
    initiated_by : Mapped[Customer] = relationship(back_populates="order_initiated", foreign_keys="Order.initiated_by_id", lazy="joined", uselist=False)
    created_by: Mapped[User] = relationship(back_populates="order_created", foreign_keys="Order.created_by_id", lazy="joined", uselist=False)
    updated_by: Mapped[Optional[User]] = relationship(back_populates="order_updated", foreign_keys="Order.updated_by_id", lazy="joined")
    invoice : Mapped[Optional[List[Invoice]]] = relationship(back_populates="order", lazy="joined")

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details )
    


class OrderDetailsLine(Base):
    __tablename__="order_detail_line"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    order_id : Mapped[int]= mapped_column(ForeignKey("order.id"))
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"))
    quantity_requested : Mapped[int]= mapped_column(default= 0)
    quantity_accorded : Mapped[int | None]= mapped_column()
    unitaryPrice : Mapped[float]= mapped_column(Numeric(18,2))  
    #stock_movement_id : Mapped[int| None]= mapped_column(ForeignKey("stockMovement.id"))
    # stock movement enclenched when purchase status set to DELIVERD
    stock_movement : Mapped[Optional[StockMovement]]= relationship(back_populates ="order_details_line", uselist=False) 
    product : Mapped[Product]= relationship(back_populates ="order_detail", uselist=False) # one line : one product
    order : Mapped[Order]= relationship(back_populates ="details", uselist=False)
    @property
    def value(self):
        return (self.quantity_requested * self.unitaryPrice)