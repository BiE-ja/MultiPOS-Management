from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from enum import Enum as pyEnum
from sqlalchemy import ForeignKey, DateTime, String, Numeric, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime, timezone


if TYPE_CHECKING:
    from backend.app.models.finance.payment import Payment
    from backend.app.models.management.unit import Area, User
    from backend.app.models.operation.stock import Product, StockMovement
    from backend.app.models.management.purchase import Order


class SaleStatus(pyEnum):
    PENDING = "pending"
    DELIVERED = "delivered"
    REJECTED = "rejected"


class Sale(Base):
    __tablename__ = "sale"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    area_id: Mapped[int] = mapped_column(ForeignKey("area.id"), nullable=False)
    reference: Mapped[str] = mapped_column(String(255), unique=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped["SaleStatus"] = mapped_column(sqlEnum(SaleStatus), nullable=False)
    created_by_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))  # the user who create the Sale
    updated_by_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))

    area: Mapped[Area] = relationship(back_populates="sale")
    customer: Mapped["Customer"] = relationship(back_populates="sale")

    created_by: Mapped[User] = relationship(
        back_populates="sale_created", foreign_keys="Sale.created_by_id", lazy="joined", uselist=False
    )
    updated_by: Mapped[Optional[User]] = relationship(
        back_populates="sale_updated", foreign_keys="Sale.updated_by_id", lazy="joined"
    )

    details: Mapped[List["SaleDetailLine"]] = relationship(back_populates="sale", cascade="all, delete-orphan")

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details)

    payments: Mapped[Payment] = relationship(back_populates="sale", lazy="joined")


class SaleDetailLine(Base):
    __tablename__ = "sale_detail_line"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sale.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int] = mapped_column()
    unitaryPrice: Mapped[float] = mapped_column(Numeric(18, 2))
    # detail line is linked to a stock movement
    # stock_movement_id : Mapped[int | None]= mapped_column(ForeignKey("stock_movement.id"), nullable=True)

    product: Mapped[Product] = relationship(back_populates="sale_detail")
    sale: Mapped[Sale] = relationship(back_populates="details")
    # stock movement enclenched if sale status set at delivered
    stock_movement: Mapped[Optional[StockMovement]] = relationship(back_populates="sale_details_line", uselist=False)

    @property
    def value(self):
        return self.quantity * self.unitaryPrice


class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    area_id: Mapped[int] = mapped_column(ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="customer")
    sale = relationship("Sale", back_populates="customer")
    order_initiated: Mapped[Optional[List[Order]]] = relationship(
        back_populates="initiated_by", foreign_keys="Order.initiated_by_id", lazy="joined"
    )
    invoice = relationship("Invoice", back_populates="customer", cascade="all, delete-orphan")
