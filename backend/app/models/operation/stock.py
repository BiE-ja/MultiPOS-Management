from __future__ import annotations

import datetime
from enum import Enum as pyEnum
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Integer, Numeric, String, ForeignKey, Enum as sqlEnum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from app.core.database import Base
from datetime import datetime, timezone


if TYPE_CHECKING:
    from backend.app.models.management.unit import Area, Employee, User
    from backend.app.models.operation.product import Product
    from backend.app.models.management.purchase import PurchaseRequestDetailsLine, OrderDetailsLine
    from backend.app.models.management.sale import SaleDetailLine
    

class InvotoryStatus(pyEnum):
    DRAFT = "draft"
    INVESTIGATING = "investigating"
    VALIDATED = "validated"

# This is used to indicate the direction of the movement
class MovementDirection(str, pyEnum):
    IN = "in"
    OUT = "out"

# This is used to indicate the type of operation performed in the movement
class MovementOperation(str, pyEnum):
    SALE = "sale_payment" # OUT
    SUPPLY = "supply" # IN
    CORRECTION = "correction_in" # IN or OUT
    RETURN_SUPPLIER = "return_supplier" # OUT
    RETURN_CUSTOMER = "return_customer" # IN
    OTHER = "other_in" # e.g in :donation or out : product broken, product out of date, product stolen etc.

class StockMovement(Base):
    __tablename__="stock_movement"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"), nullable=False)
    product_id : Mapped[int]= mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    direction : Mapped["MovementDirection"]= mapped_column(sqlEnum(MovementDirection), nullable=False)
    operation : Mapped["MovementOperation"]= mapped_column(sqlEnum(MovementOperation), nullable=False)
    quantity : Mapped[float]= mapped_column(Numeric(18,2), default=0) 
    # date where movement saved in system
    create_at : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    # real date of movement
    dateOf : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    comment : Mapped[str | None]= mapped_column(String(255)) # optional. Reason for cancellation or correction : error of tape, cause of return supplier, cause of return customer, vol, product out of date, etc.
    initiated_by_id : Mapped[int] = mapped_column(ForeignKey("employee.id"), nullable=False)
    created_by_id : Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # info of annulation
    updated_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # When the transaction was canceled
    updated_by_id : Mapped [int | None]= mapped_column(ForeignKey("user.id"))  # Nullable if not canceled
    # Relationship
    area : Mapped[Area] = relationship(back_populates="stock",uselist=False)
    product : Mapped[Product] = relationship(back_populates = "stock_movement")

    # relationship to the user who created the transaction
    created_by : Mapped[User] = relationship(back_populates="stock_movement_created", foreign_keys="StockMovement.created_by_id", lazy="joined")
    initiated_by : Mapped[Employee] = relationship(back_populates="stock_movement_initiated", foreign_keys="StockMovement.initiated_by_id", lazy="joined")
    # relationship to the user who canceled the transaction 
    updated_by : Mapped[Optional[User]] = relationship(back_populates="stock_movement_updated", foreign_keys="StockMovement.updated_by_id", lazy="joined")

    # Optionnal FK and relationship
    ###if movement is linked to a sale or linked to purchase
    sale_details_line_id : Mapped[int | None]= mapped_column(ForeignKey("sale_detail_line.id"))
    purchase_details_line_id : Mapped[int | None]= mapped_column(ForeignKey("purchase_detail_line.id"))
    order_details_line_id : Mapped[int | None]= mapped_column(ForeignKey("order_detail_line.id"))

    sale_details_line : Mapped[Optional[SaleDetailLine]] = relationship(back_populates="stock_movement",uselist=False, lazy="joined")
    purchase_details_line : Mapped[Optional[PurchaseRequestDetailsLine]] = relationship(back_populates="stock_movement",uselist=False, lazy = "joined")
    order_details_line : Mapped[Optional[OrderDetailsLine]] = relationship(back_populates="stock_movement",uselist=False, lazy = "joined")

    @validates("operation", "direction")
    def validate_coherance(self, key, value): # type: ignore 
        """ Ensure operation matches direction logic"""
        operation = value if key == "operation" else self.operation  # type: ignore
        direction = value if key == "direction" else self.direction # type: ignore

        # Only validate if both are already set
        if operation and direction:
            in_operations = {MovementOperation.SUPPLY, MovementOperation.RETURN_CUSTOMER} 
            out_operations = {MovementOperation.SALE, MovementOperation.RETURN_SUPPLIER}
            # Correction and other is flexible
            
            if direction == MovementDirection.IN and operation in out_operations:
                raise ValueError(f"Operation ' {operation} ' cannot be used with IN direction.")
            elif direction == MovementDirection.OUT and operation in in_operations:
                raise ValueError(f"Operatiion '{operation}' cannot be used with OUT direction.")
        return value # type: ignore




class Invotory(Base):
    __tablename__ = "inventory"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"), nullable=False)
    product_id : Mapped[int]= mapped_column(ForeignKey("product.id"), nullable=False)
    invotory_date : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    
    theoritical_quantity : Mapped[float]= mapped_column(default=0) 
    counted_quantity : Mapped[float]= mapped_column(default=0)
    dateOf : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    invistigation_notes : Mapped[str | None]= mapped_column(Text) # optional. Reason for cancellation or correction : error of tape, cause of return supplier, cause of return customer, vol, product out of date, etc.
    validated_quantity : Mapped[float]= mapped_column(default=0)
    investigator_id : Mapped[int| None]= mapped_column(ForeignKey("employee.id"), nullable = True)
    validated_at : Mapped[datetime | None]= mapped_column(DateTime(timezone=True)) 

    area : Mapped[Area] = relationship(back_populates="invotory", uselist=False)
    product : Mapped[Product] = relationship(back_populates="invotory", uselist=False)
    investigator: Mapped[Employee] = relationship(back_populates="invotory_problem_investigated", foreign_keys="Invotory.investigator_id", uselist=False)

