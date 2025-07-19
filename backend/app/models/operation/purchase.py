from typing import List, Optional
from enum import Enum as pyEnum
from sqlalchemy import Integer, ForeignKey, DateTime, Numeric, String, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime, timezone

from backend.app.models.deps import Area, Employee, User
from backend.app.models.operation.bill_invoice import Invoice
from backend.app.models.operation.stock import Product, StockMovement

# Ici ça représente une demande d'approvisionnement enclenché par le magasinier ou son supérieur (manager, owner)
class PurchaseRequest(Base):
    __tablename__ = "purchase_request"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    reference : Mapped[str]= mapped_column(String(255), unique= True)
    dateof : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    initiated_by_id : Mapped[int]= mapped_column(ForeignKey("employee.id")) # employee who requested the purchase
    created_by_id : Mapped[int]= mapped_column(ForeignKey("user.id")) # the user who create the PR
    updated_by_id : Mapped[int | None]= mapped_column(ForeignKey("user.id")) # PR is closed if his rejected or transformed on bill invoice
    status: Mapped["PR_status"]= mapped_column(sqlEnum("PR_status"), nullable=False)
    updated_at : Mapped[datetime | None]= mapped_column(DateTime(timezone=True))
    comments :Mapped[str | None ]= mapped_column(String(100)) 
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"))
    area : Mapped[Area] = relationship(back_populates="purchase")
    
    details : Mapped[List["PurchaseRequestDetailsLine"]] = relationship(back_populates="purchase", cascade="all, delete-orphan")
    
    initiated_by : Mapped[Employee] = relationship(back_populates="purchase", foreign_keys="PurchaseRequest.initated_by_id", lazy="joined", uselist=False)
    created_by: Mapped[User] = relationship(back_populates="purchase", foreign_keys="PurchaseRequest.created_by_id", lazy="joined", uselist=False)
    updated_by: Mapped[Optional[User]] = relationship(back_populates="purchase", foreign_keys="PurchaseRequest.updated_by_id", lazy="joined")
    invoices : Mapped[Optional[List[Invoice]]] = relationship(back_populates="purchase", lazy="joined")

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details )
    
class PR_status(pyEnum):
    OPENED = "open"
    DELIVERED = "delivered"
    CLOSED = "closed"
    REJECTED = "rejected"

class PurchaseRequestDetailsLine(Base):
    __tablename__="purchase_detail_line"
    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    purchase_id : Mapped[int]= mapped_column(ForeignKey("purchase.id"))
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"))
    quantity_requested : Mapped[int]= mapped_column(default= 0)
    quantity_accorded : Mapped[int | None]= mapped_column()
    unitaryPrice : Mapped[float]= mapped_column(Numeric(18,2))  
    stock_movement_id : Mapped[int| None]= mapped_column(ForeignKey("stockMovement.id"))
    # stock movement enclenched when purchase status set to DELIVERD
    stock_movement : Mapped[Optional[StockMovement]]= relationship(back_populate ="purchase_details_line", uselist=False) 
    product : Mapped[Product]= relationship(back_populate ="SaleDetail", uselist=False) # one line : one product
    purchase : Mapped[PurchaseRequest]= relationship(back_populate ="PurchaseDetail", uselist=False)
    @property
    def value(self):
        return (self.quantity_requested * self.unitaryPrice)
    

