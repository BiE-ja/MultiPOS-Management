from __future__ import annotations

import datetime
from enum import Enum as pyEnum
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, DateTime, Integer, Numeric, String, ForeignKey, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime, timezone

if TYPE_CHECKING:
    from backend.app.models.management.unit import Area, User
    from backend.app.models.operation.stock import Invotory
    from backend.app.models.finance.bill_invoice import Supplier
    
class PriceType (str, pyEnum):
    SALE = "sale"
    PURCHASE = "purchase"
    
class ProductCreationState(pyEnum):
    PENDING = "pending"
    VALIDED = "valided"
    REJECTED = "rejected"

class Product(Base):
    __tablename__ = "product"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    reference : Mapped[str]= mapped_column(String(50), index=True)
    name : Mapped[str]= mapped_column(String(50), index=True)
    description : Mapped[str]= mapped_column(String(100))
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"), nullable=False)
    category_id : Mapped[int | None]= mapped_column(ForeignKey("category.id")) # optional for case categorie product is delete
    purchase_price : Mapped[float]= mapped_column(Numeric(18,2), nullable = False)  # purchase price
    # actual price
    sale_price : Mapped[float]= mapped_column(Numeric(18,2), nullable = False)
    old_stock : Mapped[float]= mapped_column(Numeric(18,2), default=0)
    actual_stock : Mapped[float]= mapped_column(Numeric(18,2))
    state : Mapped["ProductCreationState"]= mapped_column(sqlEnum(ProductCreationState), nullable=False)
    area : Mapped[Area]= relationship(back_populates="product")
    product_category : Mapped[Optional["ProductCategory"]] = relationship(back_populates="product", uselist=False)
    price_history : Mapped["PriceHistory"]= relationship(back_populates="product", cascade="all, delete-orphan", lazy="joined")
    # for history of stock movement for one product
    stock_movement = relationship("StockMovement", back_populates="product")
    purchase_detail = relationship("PurchaseRequestDetailsLine", back_populates="product")
    order_detail = relationship("OrderDetailsLine", back_populates="product")
    sale_detail = relationship("SaleDetailLine", back_populates="product")
    invoice_detail = relationship("InvoiceDetailsLine", back_populates="product")
    # One supplier can have one or many product to sale
    supplier_product = relationship("Supplier_Product_List", back_populates="product")
    invotory : Mapped[Optional["Invotory"]] = relationship(back_populates="product", lazy="joined")


class ProductCategory(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index = True)
    cat_name = Column(String, index = True)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="product_category")
    product = relationship("Product", back_populates="product_category")



class PriceHistory(Base):
    __tablename__ = "price_history"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"), nullable=False) 
    type : Mapped[PriceType]= mapped_column(sqlEnum(PriceType), nullable=False)
    old_value : Mapped[float]= mapped_column(Numeric(18,2), nullable=False)
    new_value : Mapped[float]= mapped_column(Numeric(18,2), nullable=False)
    created_at : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by_id : Mapped[int]= mapped_column(ForeignKey("user.id"),nullable=False)

    product: Mapped[Product] = relationship(back_populates="price_history", uselist=False)
    created_by: Mapped[User] = relationship(back_populates="price_history", foreign_keys="PriceHistory.created_by_id", lazy="joined", uselist=False)
    
    product : Mapped[Product]= relationship(back_populates="price_history")

class Supplier_Product_List(Base):
    __tablename__="supplier_product_list"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"), nullable=False)
    supplier_id : Mapped[int]= mapped_column(ForeignKey("supplier.id"), nullable=False)

    product : Mapped[Product] = relationship(back_populates="supplier_product")
    supplier : Mapped[Supplier] = relationship(back_populates="product_list")