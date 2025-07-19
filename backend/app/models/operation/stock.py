import datetime
from enum import Enum as pyEnum
from typing import Optional
from sqlalchemy import Column, DateTime, Integer, Numeric, String, ForeignKey, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from app.database import Base
from datetime import datetime, timezone

from backend.app.models.deps import Area, User
from backend.app.models.operation.purchase import PurchaseRequest
from backend.app.models.operation.sale import Sale

class Product(Base):
    __tablename__ = "product"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    name : Mapped[str]= mapped_column(String(50), index=True)
    description : Mapped[str]= mapped_column(String(100))
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"), nullable=False)
    category_id : Mapped[int | None]= mapped_column(ForeignKey("productCategory.id")) # optional for case categorie product is delete
    # actual price
    price : Mapped[float]= mapped_column(Numeric(18,2), nullable = False)
    purchase_price : Mapped[float | None]= mapped_column(Numeric(18,2)) 
    init_stock : Mapped[int]= mapped_column(default=0)
    actual_stock : Mapped[int]= mapped_column()

    area : Mapped[Area]= relationship(back_populates="product")
    productCategory : Mapped[Optional["ProductCategory"]] = relationship(back_populates="product", uselist=False)
    price_history : Mapped["PriceHistory"]= relationship(back_populates="product", cascade="all, delete-orphan", lazy="joined")
    # for history of stock movement for one product
    stockMovement = relationship("StockMovement", back_populates="product")
    purchaseDetail = relationship("Purchase_detail", baback_populates="product")
    SaleDetail = relationship("Sale_detail", baback_populates="product")
    # One supplier can have one or many product to sale
    supplier = relationship("Supplier", back_populates="product")

class ProductCategory(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index = True)
    cat_name = Column(String, index = True)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="productcategory")
    product = relationship("Product", back_populates="productCategory")

class PriceType (str, pyEnum):
    SALE = "sale"
    PURCHASE = "purchase"

class PriceHistory(Base):
    __tablename__ = "price_history"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"), nullable=False) 
    type : Mapped[PriceType]= mapped_column(sqlEnum(PriceType), nullable=False)
    value : Mapped[float]= mapped_column(Numeric(18,2))
    dateOf : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

    product : Mapped[Product]= relationship(back_populates="priceHistory")


#########################################################################################################

    """INVENTORY"""

#########################################################################################################

class StockMovement(Base):
    __tablename__="stock_movement"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"), nullable=False)
    product_id : Mapped[int]= mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    direction : Mapped["MovementDirection"]= mapped_column(sqlEnum("MovementDirection"), nullable=False)
    operation : Mapped["MovementOperation"]= mapped_column(sqlEnum("MovemeMovementOperation"), nullable=False)
    quantity : Mapped[int]= mapped_column(default=0)
    dateOf : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    comment : Mapped[str | None]= mapped_column(String(255)) # optional. Reason for cancellation or correction : error of tape, cause of return supplier, cause of return customer, vol, product out of date, etc.
    initiated_by_id : Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # info of annulation
    cancellet_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # When the transaction was canceled
    cancelled_by_id : Mapped [int | None]= mapped_column(ForeignKey("user.id"))  # Nullable if not canceled
    # Relationship
    area : Mapped[Area] = relationship(back_populates="stock",uselist=False)
    product : Mapped[Product] = relationship(back_populate = "stock")

    # relationship to the user who created the transaction
    initiated_by : Mapped[User] = relationship(back_populates="transaction_created", foreign_keys="CashTransaction.created_by_id", lazy="joined")
    # relationship to the user who canceled the transaction 
    cancelled_by : Mapped[Optional[User]] = relationship(back_populates="transaction_cancelled", foreign_keys="CashTransaction.cancelled_by_id", lazy="joined")

    # Optionnal FK and relationship
    ###if movement is linked to a sale or linked to purchase
    sale_id : Mapped[int | None]= mapped_column(ForeignKey("sale.id"))
    purchase_id : Mapped[int | None]= mapped_column(ForeignKey("purchase.id"))

    sale : Mapped[Optional[Sale]] = relationship(back_populates="stock",uselist=False, lazy="joined")
    purchase : Mapped[Optional[PurchaseRequest]] = relationship(back_populates="stock",uselist=False, lazy = "joined")

    @validates("operation", "direction")
    def validate_coherance(self, key, value): # type: ignore 
        """ Ensure operation matches direction logic"""
        operation = value if key == "operation" else self.operation  # type: ignore
        direction = value if key == "direction" else self.direction # type: ignore

        # Only validate if both are already set
        if operation and direction:
            in_operations = {MovementOperation.SUPPLY, MovementOperation.RETURN_CUSTOMER} 
            out_operations = {MovementOperation.SALE, MovementOperation.RETURN_SUPPLIER, MovementOperation.OTHER}
            # Correction is flexible
            
            if direction == MovementDirection.IN and operation in out_operations:
                raise ValueError(f"Operation ' {operation} ' cannot be used with IN direction.")
            elif direction == MovementDirection.OUT and operation in in_operations:
                raise ValueError(f"Operatiion '{operation}' cannot be used with OUT direction.")
        return value # type: ignore

# This is used to indicate the direction of the movement
class MovementDirection(str, pyEnum):
    IN = "in"
    OUT = "out"

# This is used to indicate the type of operation performed in the movement
class MovementOperation(str, pyEnum):
    SALE = "sale_payment" # OUT
    SUPPLY = "supply" # IN
    CORRECTION = "correction" # IN or OUT
    RETURN_SUPPLIER = "return_supplier" # OUT
    RETURN_CUSTOMER = "return_customer" # IN
    OTHER = "other" # product broken, product out of date, product stolen etc.