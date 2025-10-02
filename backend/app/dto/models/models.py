from enum import Enum as pyEnum
import uuid
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String, Enum as sqlEnum, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from typing import Any, List, Optional
from datetime import datetime, timezone


# Represente a point of sale
class Area(Base):
    __tablename__ = "area"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(50), index=True)
    location = Column(String(255))

    owners = relationship("User", secondary="area_owners", back_populates="owned_areas")
    employee = relationship("Employee", back_populates="area", cascade="all, delete-orphan")
    roles = relationship("Role", back_populates="area", cascade="all, delete-orphan")

    customer = relationship("Customer", back_populates="area", cascade="all, delete-orphan")
    product = relationship("Product", back_populates="area", cascade="all, delete-orphan")
    product_category = relationship("ProductCategory", back_populates="area", cascade="all, delete-orphan")
    purchase = relationship("PurchaseRequest", back_populates="area", cascade="all, delete-orphan")
    sale = relationship("Sale", back_populates="area", cascade="all, delete-orphan")
    order = relationship("Order", back_populates="area", cascade="all, delete-orphan")
    supplier = relationship("Supplier", back_populates="area", cascade="all, delete-orphan")
    cash_register = relationship("CashAccount", back_populates="area", cascade="all, delete-orphan")
    stock = relationship("StockMovement", back_populates="area", cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates="area", cascade="all, delete-orphan")
    invotory = relationship("Invotory", back_populates="area", cascade="all, delete-orphan")
    log = relationship("Log", back_populates="area")


class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)

    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    adress: Mapped[str | None] = mapped_column(String(255))

    # the Area where employee is affiliate
    area = relationship("Area", back_populates="employee")
    # optional one-to-one relationship with user
    user: Mapped[Optional["User"]] = relationship(back_populates="employee", uselist=False)
    purchase_initiated: Mapped[List["PurchaseRequest"]] = relationship(
        back_populates="initiated_by",
        foreign_keys="PurchaseRequest.initiated_by_id",
    )
    invoice_initiated: Mapped[Optional[List["Invoice"]]] = relationship(
        back_populates="initiated_by",
        foreign_keys="Invoice.initiated_by_id",
    )
    stock_movement_initiated: Mapped[Optional[List["StockMovement"]]] = relationship(
        back_populates="initiated_by", foreign_keys="StockMovement.initiated_by_id"
    )
    invotory_problem_investigated: Mapped[Optional[List["Invotory"]]] = relationship(
        back_populates="investigator", foreign_keys="Invotory.investigator_id"
    )


class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_owner: Mapped[bool] = mapped_column(default=False)
    is_password_reinitialized: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # To log the user's actions
    log = relationship("Log", back_populates="user")

    employee_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("employee.id"), unique=True)
    employee: Mapped[Optional["Employee"]] = relationship(back_populates="user", uselist=False)
    owned_areas = relationship("Area", secondary="area_owners", back_populates="owners")

    adjustements_done: Mapped[Optional["CashAdjustement"]] = relationship(
        back_populates="performed_by",
        foreign_keys="CashAdjustement.performed_by_id",
    )

    transaction_created: Mapped[Optional[List["CashTransaction"]]] = relationship(
        back_populates="created_by",
        foreign_keys="CashTransaction.created_by_id",
    )
    transaction_updated: Mapped[Optional[List["CashTransaction"]]] = relationship(
        back_populates="updated_by",
        foreign_keys="CashTransaction.updated_by_id",
    )

    stock_movement_created: Mapped[Optional[List["StockMovement"]]] = relationship(
        back_populates="created_by",
        foreign_keys="StockMovement.created_by_id",
    )
    stock_movement_updated: Mapped[Optional[List["StockMovement"]]] = relationship(
        back_populates="updated_by",
        foreign_keys="StockMovement.updated_by_id",
    )

    purchase_created: Mapped[Optional[List["PurchaseRequest"]]] = relationship(
        back_populates="created_by",
        foreign_keys="PurchaseRequest.created_by_id",
    )
    purchase_updated: Mapped[Optional[List["PurchaseRequest"]]] = relationship(
        back_populates="updated_by",
        foreign_keys="PurchaseRequest.updated_by_id",
    )

    order_created: Mapped[Optional[List["Order"]]] = relationship(
        back_populates="created_by", foreign_keys="Order.created_by_id"
    )
    order_updated: Mapped[Optional[List["Order"]]] = relationship(
        back_populates="updated_by", foreign_keys="Order.updated_by_id"
    )

    sale_created: Mapped[Optional[List["Sale"]]] = relationship(
        back_populates="created_by", foreign_keys="Sale.created_by_id"
    )
    sale_updated: Mapped[Optional[List["Sale"]]] = relationship(
        back_populates="updated_by", foreign_keys="Sale.updated_by_id"
    )

    invoice_created: Mapped[Optional[List["Invoice"]]] = relationship(
        back_populates="created_by", foreign_keys="Invoice.created_by_id"
    )
    invoice_updated: Mapped[Optional[List["Invoice"]]] = relationship(
        back_populates="updated_by", foreign_keys="Invoice.updated_by_id"
    )

    price_history: Mapped[Optional[List["PriceHistory"]]] = relationship(
        back_populates="created_by",
        foreign_keys="PriceHistory.created_by_id",
    )
    # Optionnal relationship
    # register_id : Mapped[int | None] = mapped_column(ForeignKey("cash_account.id"))
    cash_register: Mapped[Optional["CashAccount"]] = relationship(back_populates="user")

    # role assigned for user (one or more role). ex : manager, account, saler, logistician,..
    roles: Mapped[List["Role"]] = relationship(secondary="user_roles", back_populates="users", lazy="joined")


class Role(Base):
    __tablename__ = "role"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)  # name can be : manager, accountant, saler, storekeeper...
    description = Column(String(255))
    users = relationship("User", secondary="user_roles", back_populates="roles")
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="roles")


# Association table

user_role = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("role.id"), primary_key=True),
)

# Association table between user and area
# user (if his owner can be have one-or-more area)
area_owners = Table(
    "area_owners",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("area_id", UUID(as_uuid=True), ForeignKey("area.id"), primary_key=True),
)


class PriceType(str, pyEnum):
    SALE = "sale"
    PURCHASE = "purchase"


class ProductCreationState(pyEnum):
    PENDING = "pending"
    VALIDED = "valided"
    REJECTED = "rejected"


class Product(Base):
    __tablename__ = "product"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    reference: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(String(100))
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("category.id")
    )  # optional for case categorie product is delete
    purchase_price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)  # purchase price
    # actual price
    sale_price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    old_stock: Mapped[float] = mapped_column(Numeric(18, 2), default=0)
    actual_stock: Mapped[float] = mapped_column(Numeric(18, 2))
    state: Mapped["ProductCreationState"] = mapped_column(sqlEnum(ProductCreationState), nullable=False)
    area: Mapped[Area] = relationship(back_populates="product")
    product_category: Mapped[Optional["ProductCategory"]] = relationship(back_populates="product", uselist=False)
    price_history: Mapped["PriceHistory"] = relationship(back_populates="product", cascade="all, delete-orphan")
    # for history of stock movement for one product
    stock_movement = relationship("StockMovement", back_populates="product")
    purchase_detail = relationship("PurchaseRequestDetailsLine", back_populates="product")
    order_detail = relationship("OrderDetailsLine", back_populates="product")
    sale_detail = relationship("SaleDetailLine", back_populates="product")
    invoice_detail = relationship("InvoiceDetailsLine", back_populates="product")
    # One supplier can have one or many product to sale
    supplier_product = relationship("Supplier_Product_List", back_populates="product")
    invotory: Mapped[Optional["Invotory"]] = relationship(back_populates="product")
    lots: Mapped[Optional["Lot"]] = relationship(back_populates="product")


class ProductCategory(Base):
    __tablename__ = "category"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    cat_name = Column(String, index=True)
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="product_category")
    product = relationship("Product", back_populates="product_category")


class PriceHistory(Base):
    __tablename__ = "price_history"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"), nullable=False)
    type: Mapped[PriceType] = mapped_column(sqlEnum(PriceType), nullable=False)
    old_value: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    new_value: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    product: Mapped[Product] = relationship(back_populates="price_history", uselist=False)
    created_by: Mapped[User] = relationship(
        back_populates="price_history", foreign_keys="PriceHistory.created_by_id", lazy="joined", uselist=False
    )

    product: Mapped[Product] = relationship(back_populates="price_history")


class Lot(Base):
    __tablename__ = "lot"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    lot_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"), nullable=False)
    initial_quantity: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    actual_quantity: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    perimed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    product: Mapped[Product] = relationship(back_populates="lots", uselist=False)
    stock_movement: Mapped[Optional["StockMovement"]] = relationship(back_populates="product_lot", uselist=False)


class Supplier_Product_List(Base):
    __tablename__ = "supplier_product_list"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"), nullable=False)
    supplier_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("supplier.id"), nullable=False)

    product: Mapped[Product] = relationship(back_populates="supplier_product")
    supplier: Mapped["Supplier"] = relationship(back_populates="product_list")


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
    SALE = "sale_payment"  # OUT
    SUPPLY = "supply"  # IN
    CORRECTION = "correction_in"  # IN or OUT
    RETURN_SUPPLIER = "return_supplier"  # OUT
    RETURN_CUSTOMER = "return_customer"  # IN
    OTHER = "other_in"  # e.g in :donation or out : product broken, product out of date, product stolen etc.


class StockMovement(Base):
    __tablename__ = "stock_movement"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"), nullable=False)
    direction: Mapped["MovementDirection"] = mapped_column(sqlEnum(MovementDirection), nullable=False)
    operation: Mapped["MovementOperation"] = mapped_column(sqlEnum(MovementOperation), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(18, 2), default=0)
    lot_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("lot.id"))  # optional
    # date where movement saved in system
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # real date of movement
    dateOf: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    comment: Mapped[str | None] = mapped_column(String(255))  # optional. Reason for cancellation or correction :
    # error of tape, cause of return supplier,
    # cause of return customer, vol, product out of date, etc.

    initiated_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employee.id"), nullable=False)
    created_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    # info of annulation
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # When the transaction was canceled
    updated_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )  # Nullable if not canceled
    # Relationship
    area: Mapped[Area] = relationship(back_populates="stock", uselist=False)
    product: Mapped[Product] = relationship(back_populates="stock_movement")
    product_lot: Mapped[Optional[Lot]] = relationship(back_populates="stock_movement", uselist=False)

    # relationship to the user who created the transaction
    created_by: Mapped[User] = relationship(
        back_populates="stock_movement_created", foreign_keys="StockMovement.created_by_id", lazy="joined"
    )
    initiated_by: Mapped[Employee] = relationship(
        back_populates="stock_movement_initiated", foreign_keys="StockMovement.initiated_by_id", lazy="joined"
    )
    # relationship to the user who canceled the transaction
    updated_by: Mapped[Optional[User]] = relationship(
        back_populates="stock_movement_updated", foreign_keys="StockMovement.updated_by_id", lazy="joined"
    )

    # Optionnal FK and relationship
    # if movement is linked to a sale or linked to purchase
    sale_details_line_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sale_detail_line.id")
    )
    purchase_details_line_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("purchase_detail_line.id")
    )
    order_details_line_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("order_detail_line.id")
    )

    sale_details_line: Mapped[Optional["SaleDetailLine"]] = relationship(
        back_populates="stock_movement", uselist=False, lazy="joined"
    )
    purchase_details_line: Mapped[Optional["PurchaseRequestDetailsLine"]] = relationship(
        back_populates="stock_movement", uselist=False, lazy="joined"
    )
    order_details_line: Mapped[Optional["OrderDetailsLine"]] = relationship(
        back_populates="stock_movement", uselist=False, lazy="joined"
    )

    @validates("operation", "direction")
    def validate_coherance(self, key, value):  # type: ignore
        """Ensure operation matches direction logic"""
        operation = value if key == "operation" else self.operation  # type: ignore
        direction = value if key == "direction" else self.direction  # type: ignore

        # Only validate if both are already set
        if operation and direction:
            in_operations = {MovementOperation.SUPPLY, MovementOperation.RETURN_CUSTOMER}
            out_operations = {MovementOperation.SALE, MovementOperation.RETURN_SUPPLIER}
            # Correction and other is flexible

            if direction == MovementDirection.IN and operation in out_operations:
                raise ValueError(f"Operation ' {operation} ' cannot be used with IN direction.")
            elif direction == MovementDirection.OUT and operation in in_operations:
                raise ValueError(f"Operatiion '{operation}' cannot be used with OUT direction.")
        return value  # type: ignore


class Invotory(Base):
    __tablename__ = "inventory"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"), nullable=False)
    invotory_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    theoritical_quantity: Mapped[float] = mapped_column(default=0)
    counted_quantity: Mapped[float] = mapped_column(default=0)
    dateOf: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # optional. Reason for cancellation or correction :
    # error of tape, cause of return supplier, cause of return customer, vol, product out of date, etc.
    invistigation_notes: Mapped[str | None] = mapped_column(Text)
    validated_quantity: Mapped[float] = mapped_column(default=0)
    investigator_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employee.id"), nullable=True
    )
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    area: Mapped[Area] = relationship(back_populates="invotory", uselist=False)
    product: Mapped[Product] = relationship(back_populates="invotory", uselist=False)
    investigator: Mapped[Employee] = relationship(
        back_populates="invotory_problem_investigated", foreign_keys="Invotory.investigator_id", uselist=False
    )


class SaleStatus(pyEnum):
    PENDING = "pending"
    DELIVERED = "delivered"
    REJECTED = "rejected"


class Sale(Base):
    __tablename__ = "sale"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customer.id"))
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)
    reference: Mapped[str] = mapped_column(String(255), unique=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped["SaleStatus"] = mapped_column(sqlEnum(SaleStatus), nullable=False)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )  # the user who create the Sale
    updated_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))

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

    payments: Mapped["Payment"] = relationship(back_populates="sale", lazy="joined")


class SaleDetailLine(Base):
    __tablename__ = "sale_detail_line"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    sale_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sale.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"))
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
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="customer")
    sale = relationship("Sale", back_populates="customer")
    order_initiated: Mapped[Optional[List["Order"]]] = relationship(
        back_populates="initiated_by", foreign_keys="Order.initiated_by_id", lazy="joined"
    )
    invoice = relationship("Invoice", back_populates="customer", cascade="all, delete-orphan")


class Request_status(pyEnum):
    OPENED = "open"
    DELIVERED = "delivered"
    CLOSED = "closed"
    REJECTED = "rejected"


# Ici ça représente une demande d'approvisionnement enclenché par le magasinier ou son supérieur (manager, owner)
class PurchaseRequest(Base):
    __tablename__ = "purchase_request"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    reference: Mapped[str] = mapped_column(String(255), unique=True)
    dateof: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    initiated_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employee.id")
    )  # employee who requested the purchase
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )  # the user who create the PR
    updated_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )  # PR is closed if his rejected or transformed on bill invoice
    status: Mapped["Request_status"] = mapped_column(sqlEnum(Request_status), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    comments: Mapped[str | None] = mapped_column(String(100))
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"))
    area: Mapped[Area] = relationship(back_populates="purchase")

    details: Mapped[List["PurchaseRequestDetailsLine"]] = relationship(
        back_populates="purchase", cascade="all, delete-orphan"
    )

    initiated_by: Mapped[Employee] = relationship(
        back_populates="purchase_initiated",
        foreign_keys="PurchaseRequest.initiated_by_id",
        lazy="joined",
        uselist=False,
    )
    created_by: Mapped[User] = relationship(
        back_populates="purchase_created", foreign_keys="PurchaseRequest.created_by_id", lazy="joined", uselist=False
    )
    updated_by: Mapped[Optional[User]] = relationship(
        back_populates="purchase_updated", foreign_keys="PurchaseRequest.updated_by_id", lazy="joined"
    )
    invoice: Mapped[Optional[List["Invoice"]]] = relationship(back_populates="purchase", lazy="joined")

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details)


class PurchaseRequestDetailsLine(Base):
    __tablename__ = "purchase_detail_line"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    purchase_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("purchase_request.id"))
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"))
    quantity_requested: Mapped[int] = mapped_column(default=0)
    quantity_accorded: Mapped[int | None] = mapped_column()
    unitaryPrice: Mapped[float] = mapped_column(Numeric(18, 2))
    # stock_movement_id : Mapped[int| None]= mapped_column(ForeignKey("stockMovement.id"))
    # stock movement enclenched when purchase status set to DELIVERD
    stock_movement: Mapped[Optional[StockMovement]] = relationship(
        back_populates="purchase_details_line", uselist=False
    )
    product: Mapped[Product] = relationship(back_populates="purchase_detail", uselist=False)  # one line : one product
    purchase: Mapped[PurchaseRequest] = relationship(back_populates="details", uselist=False)

    @property
    def value(self):
        return self.quantity_requested * self.unitaryPrice


class Order(Base):
    __tablename__ = "order"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    reference: Mapped[str] = mapped_column(String(255), unique=True)
    dateof: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    initiated_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customer.id")
    )  # customer who requested the order
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )  # the user who put the order in system
    updated_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )  # order is closed if his rejected or transformed on bill invoice outgoing
    status: Mapped["Request_status"] = mapped_column(sqlEnum(Request_status), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    comments: Mapped[str | None] = mapped_column(String(100))
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"))
    area: Mapped[Area] = relationship(back_populates="order")

    details: Mapped[List["OrderDetailsLine"]] = relationship(back_populates="order", cascade="all, delete-orphan")

    initiated_by: Mapped[Customer] = relationship(
        back_populates="order_initiated", foreign_keys="Order.initiated_by_id", lazy="joined", uselist=False
    )
    created_by: Mapped[User] = relationship(
        back_populates="order_created", foreign_keys="Order.created_by_id", lazy="joined", uselist=False
    )
    updated_by: Mapped[Optional[User]] = relationship(
        back_populates="order_updated", foreign_keys="Order.updated_by_id", lazy="joined"
    )
    invoice: Mapped[Optional[List["Invoice"]]] = relationship(back_populates="order", lazy="joined")

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details)


class OrderDetailsLine(Base):
    __tablename__ = "order_detail_line"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    order_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey("order.id"))
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"))
    quantity_requested: Mapped[int] = mapped_column(default=0)
    quantity_accorded: Mapped[int | None] = mapped_column()
    unitaryPrice: Mapped[float] = mapped_column(Numeric(18, 2))
    # stock_movement_id : Mapped[int| None]= mapped_column(ForeignKey("stockMovement.id"))
    # stock movement enclenched when purchase status set to DELIVERD
    stock_movement: Mapped[Optional[StockMovement]] = relationship(back_populates="order_details_line", uselist=False)
    product: Mapped[Product] = relationship(back_populates="order_detail", uselist=False)  # one line : one product
    order: Mapped[Order] = relationship(back_populates="details", uselist=False)

    @property
    def value(self):
        return self.quantity_requested * self.unitaryPrice


class PaymentMethod(pyEnum):
    CARD = "card"
    CHECK = "check"
    CASH = "cash"
    WIRE = "wire"


class TransactionType(pyEnum):
    IN = "in"
    OUT = "out"


class TransactionState(pyEnum):
    # e.g le chèque client a été déposé à la banque
    # ou le chèque a été remis au fournisseur (cas chèque sortant :achat)
    # e.g la somme d'argent a été remis à un employé (en attente facture)
    # virement en faveur d'un fournisseur déposé à la banque
    # bon de commande reçue d'un client et produit livré
    PENDING = "pending"
    # espèce reçue (client), facture reçue(employé),
    # constat sur relevé bancaire du virement (en faveur d'un client ou sortant en faveur d'un fournisseur)
    # constat sur relevé bancaire chèque touché par un fournisseur ou validation d'un chèque déposé
    FINALIZED = "finalized"
    # vente validé mais pas encore payé
    # (cas où c'est un autre employé qui saisie la vente et le paiement se fait à la caisse)
    # bon de commande émis
    # demande de retrait au caisse émis par un employé (pas encore décaissé)
    OPENED = "opened"
    # a transaction taged "closed" can't be updated or rejected
    CLOSED = "closed"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
    # a transaction can be canceled if his date of creation is date of day else the transcation may be rejected
    CANCELED = "canceled"
    REJECTED = "rejected"


# Represent a payment made  (can be cash, card, etc.)
class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    reference: Mapped[str | None] = mapped_column()
    amount: Mapped[float] = mapped_column(Numeric(18, 2))  # Amount of the payment
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    method: Mapped["PaymentMethod"] = mapped_column(sqlEnum(PaymentMethod), nullable=False)  # ex : cash, card, etc.
    state: Mapped["TransactionState"] = mapped_column(sqlEnum(TransactionState), nullable=False)
    direction: Mapped["TransactionType"] = mapped_column(sqlEnum(TransactionType), nullable=False)
    sale_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("sale.id"), nullable=False)
    invoice_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("invoice.id"), nullable=False)
    # Optional FK if the payment is linked to a cash transaction
    # If the payment is not linked to a cash transaction, this can be None
    cash_transac_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cash_transaction.id"), nullable=True
    )

    cash_transaction: Mapped[Optional["CashTransaction"]] = relationship(
        back_populates="payments", uselist=False, lazy="joined"
    )
    # Reverse relation from sale, payment
    sale: Mapped[Optional["Sale"]] = relationship(back_populates="payments", uselist=False, lazy="joined")
    invoice: Mapped[Optional[List["Invoice"]]] = relationship(back_populates="payments", uselist=False, lazy="joined")


# This is used to indicate the direction of the transaction
class TransactionDirection(str, pyEnum):
    IN = "in"
    OUT = "out"


# This is used to indicate the type of operation performed in the transaction
class TransactionPurpose(str, pyEnum):
    SALE_PAYMENT = "sale_payment"  # IN
    SUPPLY = "supply"  # OUT
    CORRECTION_IN = "correction_in"  # IN or OUT # may be retour de fonds (versement reliquat : achat urgent)
    CORRECTION_OUT = "correction_out"
    BANK_TRANSFERT = "bank_transfert"  # OUT
    MISC_EXPENSE_IN = "misc_expense_in"  # IN or OUT
    MISC_EXPENSE_OUT = "misc_expense_out"


class CashAccountState(str, pyEnum):
    OPEN = "open"
    CLOSED = "closed"
    BALANCED = "balanced"
    NOT_BALANCED = "not_balanced"
    BALANCED_FORCED = "balanced_forced"


class CashAdjustementType(str, pyEnum):
    OPENING = "opening"
    BALANCING = "balancing"
    FORCING_BALANCE = "forcing_balance"


# Represent an actual movement of money "in" or "out" of the cash register
# This can be a payment for a sale, a cash deposit, or a cash withdrawal"""
class CashTransaction(Base):
    """Represent an actual movement of money in or out of the cash register\n
    This can be a payment for a sale, a cash deposit, or a cash withdrawal
    """

    __tablename__ = "cash_transaction"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    direction: Mapped[TransactionDirection] = mapped_column(sqlEnum(TransactionDirection), nullable=False)
    operation: Mapped[TransactionPurpose] = mapped_column(sqlEnum(TransactionPurpose), nullable=False)
    status: Mapped[TransactionState] = mapped_column(
        sqlEnum(TransactionState), default=TransactionState.PENDING, nullable=False
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # info of update
    updated_reason: Mapped[str | None] = mapped_column(String(255))  # Reason for cancellation or correction
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # When the transaction was canceled
    updated_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id")
    )  # Nullable if not canceled

    register_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cash_account.id"), nullable=False)
    payment_ref: Mapped[str | None] = mapped_column(String(50))
    # Date of the transaction
    dateOf: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    register: Mapped["CashAccount"] = relationship(back_populates="transactions", lazy="joined", uselist=False)
    details: Mapped[List["CashTransactionDetailsLine"]] = relationship(
        back_populates="transaction", cascade="all, delete-orphan"
    )
    # relationship to the user who created the transaction
    created_by: Mapped["User"] = relationship(
        back_populates="transaction_created", foreign_keys="CashTransaction.created_by_id", lazy="joined"
    )
    # relationship to the user who canceled the transaction
    updated_by: Mapped[Optional["User"]] = relationship(
        back_populates="transaction_updated", foreign_keys="CashTransaction.updated_by_id", lazy="joined"
    )
    # relationship to the payment if it exists
    payments: Mapped[Optional["Payment"]] = relationship(
        back_populates="cash_transaction", uselist=False, lazy="joined"
    )

    # --- Useful helper ---
    @property
    def is_valid(self):
        """Check if the transaction is valid (not canceled or failed)"""
        return self.status == TransactionState.COMPLETED

    @property
    def cancel(self):
        """Cancel the transaction (does not delete it)"""
        """Cancels the transaction if it is valid."""
        if not self.is_valid:
            raise ValueError("This transaction is already canceled.")
        if self.operation == TransactionPurpose.SALE_PAYMENT:
            raise ValueError("Sale payments cannot be canceled directly.")
        self.state = TransactionState.CANCELED

    @property
    def total_amount(self):
        """get the amount of transaction"""
        """Amount of the transaction (can be positive or negative depending on the direction)"""
        amount = sum(detail.value for detail in self.details)
        if self.direction == TransactionDirection.OUT:
            amount = amount * (-1)
        return amount

    @validates("operation", "direction")
    def validate_coherance(self, key, value):  # type: ignore
        """Ensure operation matches direction logic"""
        operation = value if key == "operation" else self.operation  # type: ignore
        direction = value if key == "direction" else self.direction  # type: ignore

        # Only validate if both are already set
        if operation and direction:
            in_operations = {
                TransactionPurpose.SALE_PAYMENT,
                TransactionPurpose.SUPPLY,
                TransactionPurpose.CORRECTION_IN,
                TransactionPurpose.MISC_EXPENSE_IN,
            }
            out_operations = {
                TransactionPurpose.BANK_TRANSFERT,
                TransactionPurpose.CORRECTION_OUT,
                TransactionPurpose.MISC_EXPENSE_OUT,
            }
            # Correction is flexible,misc expens is flexible (cas versement reliquat)

            if direction == TransactionDirection.IN and operation in out_operations:
                raise ValueError(f"Operation ' {operation} ' cannot be used with IN direction.")
            elif direction == TransactionDirection.OUT and operation in in_operations:
                raise ValueError(f"Operatiion '{operation}' cannot be used with OUT direction.")
        return value  # type: ignore


# e.g : 20.000 * 5
class CashTransactionDetailsLine(Base):
    __tablename__ = "transaction_details_line"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    transac_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cash_transaction.id"), nullable=False, unique=True
    )
    denomination_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("denomination.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer)

    transaction: Mapped[CashTransaction] = relationship(back_populates="details", uselist=False)
    denomination: Mapped["Denomination"] = relationship(back_populates="transaction_line", uselist=False)

    @property
    def amount(self):
        return self.quantity * self.denomination.value


# This class represent a bank billet
class Denomination(Base):
    __tablename__ = "denomination"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(10), unique=True)  # e.g., "20000", "10000", etc.
    value: Mapped[float] = mapped_column(Numeric(18, 2))  # because value can be 0,20 Ar or 0,50 USD
    currency: Mapped[str] = mapped_column(String(10))

    adjustement_line: Mapped["CashAdjustementLine"] = relationship(back_populates="denomination")
    transaction_line: Mapped["CashTransactionDetailsLine"] = relationship(back_populates="denomination")

    def __repr__(self):
        return f"<Denomination(name={self.name}, value={self.value})>"


# Represent a signle cash account (like a bank or  cash register)
class CashAccount(Base):
    __tablename__ = "cash_account"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    amount_init: Mapped[float] = mapped_column(Numeric(18, 2))
    state: Mapped[CashAccountState] = mapped_column(
        sqlEnum(CashAccountState), nullable=False
    )  # state : open, closed, balanced, notBalanced, balanced_forced
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"))
    # amount edited by employee during balancing
    balancing_amount: Mapped[float] = mapped_column(Numeric(18, 2))

    # Relationship
    adjustement: Mapped["CashAdjustement"] = relationship(
        back_populates="cash_register", uselist=False, cascade="all, delete-orphan"
    )

    transactions: Mapped[List["CashTransaction"]] = relationship(
        back_populates="register", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship(back_populates="cash_register")
    area: Mapped["Area"] = relationship(back_populates="cash_register")


class CashAdjustement(Base):
    __tablename__ = "cash_adjustement"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    register_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cash_account.id"), nullable=False)
    performed_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    typeOf: Mapped["CashAdjustementType"] = mapped_column(
        sqlEnum(CashAdjustementType), nullable=False
    )  # reason for adjustment : opening, closing, correction
    dateof: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    cash_register: Mapped["CashAccount"] = relationship(back_populates="adjustement")
    performed_by: Mapped["User"] = relationship(
        back_populates="adjustements_done", foreign_keys="CashAdjustement.performed_by_id", lazy="joined"
    )
    details: Mapped[List["CashAdjustementLine"]] = relationship(
        back_populates="adjustement", cascade="all, delete-orphan"
    )

    @property
    def total_amount(self) -> float:
        return sum(detail.value for detail in self.details)


# e.g : 20.000 * 5
class CashAdjustementLine(Base):
    __tablename__ = "cash_adjustement_line"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    adjustement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cash_adjustement.id"), nullable=False
    )
    denomination_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("denomination.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer)

    denomination: Mapped[Denomination] = relationship(back_populates="adjustement_line", uselist=False)
    adjustement: Mapped["CashAdjustement"] = relationship(back_populates="details")

    @property
    def amount(self):
        return self.quantity * self.denomination.value


# Represents an invoice for purchases or sales
# It can be an incoming invoice (from a supplier) or an outgoing invoice (for a customer)
# It can be linked to a purchase request or a sale
class Invoice(Base):
    __tablename__ = "invoice"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    ref: Mapped[str | None] = mapped_column(String(50))
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"))
    dateof: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    initiated_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employee.id"), nullable=False)
    created_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    updated_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    type: Mapped["TransactionType"] = mapped_column(sqlEnum(TransactionType), nullable=False)
    status: Mapped["TransactionState"] = mapped_column(sqlEnum(TransactionState), nullable=False)
    comments: Mapped[str | None] = mapped_column(String(255))
    amount_payed: Mapped[float | None] = mapped_column(Numeric(18, 2), default=0.0)

    # optional FK (if invoice received)
    purchase_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("purchase_request.id"))
    # optional FK (if invoice sent)
    order_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("order.id"))

    # payment_id : Mapped[int | None]= mapped_column(ForeignKey("payments.id"))

    supplier_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("supplier.id"))
    customer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("customer.id"))

    area: Mapped[Area] = relationship(back_populates="invoice")
    supplier: Mapped[Optional["Supplier"]] = relationship(back_populates="invoice", uselist=False)
    customer: Mapped[Optional["Customer"]] = relationship(back_populates="invoice", uselist=False)

    purchase: Mapped[Optional[PurchaseRequest]] = relationship(back_populates="invoice", uselist=False)
    order: Mapped[Optional[Order]] = relationship(back_populates="invoice", uselist=False)
    # payment is optional, if invoice is not paid yet
    payments: Mapped[Optional[Payment]] = relationship(back_populates="invoice", lazy="joined")

    initiated_by: Mapped[Employee] = relationship(
        back_populates="invoice_initiated", foreign_keys="Invoice.initiated_by_id", lazy="joined", uselist=False
    )
    created_by: Mapped[User] = relationship(
        back_populates="invoice_created", foreign_keys="Invoice.created_by_id", lazy="joined", uselist=False
    )
    updated_by: Mapped[Optional[User]] = relationship(
        back_populates="invoice_updated", foreign_keys="Invoice.updated_by_id", lazy="joined"
    )

    details: Mapped[List["InvoiceDetailsLine"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")
    # Optional FK stock movement, enclenched if purchase status is delivered

    @property
    def total_amount(self):
        return sum(detail.value for detail in self.details)

    @property
    def amount_to_pay(self):
        return sum(detail.amount_payable for detail in self.details)

    @validates("status", "amount_payed")
    def validate_coherance(self, key, value) -> Any:  # type: ignore
        amount_payed = self.amount_payed
        if amount_payed is None:
            amount_payed = 0
        if key == "status":
            if value == TransactionState.CLOSED and amount_payed < self.amount_to_pay:
                raise ValueError("Cannot close invoice, amount paid is less than amount to pay")
            if value == TransactionState.REJECTED and amount_payed > 0:
                raise ValueError("Cannot reject invoice, amount paid is greater than zero")
        elif key == "amount_payed":
            if value < 0 or value > self.amount_to_pay:
                raise ValueError("Amount paid must be between 0 and total amount to pay")
        return value  # type: ignore


class InvoiceDetailsLine(Base):
    __tablename__ = "invoice_details_line"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("invoice.id"))
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"))
    quantity_requested: Mapped[int] = mapped_column(default=0)
    quantity_real: Mapped[int | None] = mapped_column(Integer)  # sended or receeived
    unitaryPrice: Mapped[float] = mapped_column(Numeric(18, 2))

    product: Mapped[Product] = relationship(back_populates="invoice_detail", uselist=False)  # one line : one product
    invoice: Mapped[Invoice] = relationship(back_populates="details", uselist=False)

    @property
    def value(self):
        return self.quantity_requested * self.unitaryPrice

    @property
    def amount_payable(self):
        amount = 0
        if self.quantity_real is not None:
            amount = self.quantity_real * self.unitaryPrice
        return amount


class Supplier(Base):
    __tablename__ = "supplier"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)

    area: Mapped[Area] = relationship(back_populates="supplier")
    product_list: Mapped[List[Supplier_Product_List]] = relationship(back_populates="supplier")
    invoice: Mapped[List[Invoice]] = relationship(back_populates="supplier")


class Log(Base):
    __tablename__ = "log"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    dateAction = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    area_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("area.id"), nullable=False)
    action = Column(String)

    user = relationship("User", back_populates="log")
    area = relationship("Area", back_populates="log")
