from typing import List, Optional
from enum import Enum as pyEnum
from sqlalchemy import ForeignKey, DateTime, String, Numeric, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime, timezone

from backend.app.models.deps import Area
from backend.app.models.finance.payment import Payment
from backend.app.models.operation.bill_invoice import Invoice
from backend.app.models.operation.stock import Product, StockMovement


class Sale(Base):
    __tablename__ = "sale"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    customer_id : Mapped[int]= mapped_column(ForeignKey("customer.id"))
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"), nullable=False)
    reference : Mapped[str]= mapped_column(String(255), unique= True)
    date : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    status:Mapped["SaleStatus"] = mapped_column(sqlEnum("SaleStatus"), nullable=False)
    area : Mapped[Area]= relationship(back_populates="sale")
    customer : Mapped["Customer"] = relationship(back_populate ="Sale")
    details : Mapped[List["SaleDetailLine"]] = relationship(back_populates="Sale", cascade="all, delete-orphan")
    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details )

    payment : Mapped[Payment]= relationship(back_populates="sale", lazy="joined")
    invoice : Mapped[Optional["Invoice"]] = relationship(back_populates="sale", uselist=False, lazy="joined")
        

class SaleDetailLine(Base):
    __tablename__="sale_detail_line"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    sale_id : Mapped[int]= mapped_column(ForeignKey("sale.id"), nullable=False)
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"))
    quantity : Mapped[int]= mapped_column()
    unitaryPrice : Mapped[float]= mapped_column(Numeric(18,2)) 
    # detail line is linked to a stock movement
    stockMovement_id : Mapped[int | None]= mapped_column(ForeignKey("stock_movement.id"), nullable=True)

    product : Mapped[Product] = relationship(back_populate ="sale_details_line")
    sale : Mapped[Sale]= relationship(back_populate ="sale_details_line")
    # stock movement enclenched if sale status set at delivered
    stockMovement : Mapped[Optional[StockMovement]]= relationship(back_populate ="sale_details_line", uselist=False)
    @property
    def value(self):
        return (self.quantity * self.unitaryPrice)

class SaleStatus(pyEnum):
    PENDING = "pending"
    DELIVERED = "delivered"
    REJECTED = "rejected"

class Customer(Base):
    __tablename__ = "customer"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    name : Mapped[str]= mapped_column(String(255), unique= True)
    email : Mapped[str]= mapped_column(String(50), unique= True)
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"),nullable=False)
    
    area = relationship("Area", back_populates="customer")
    sale = relationship("Sale", back_populates="customer")
    invoice = relationship("Invoice", back_populates="customer", cascade="all, delete-orphan", optional=True)