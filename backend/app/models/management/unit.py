from __future__ import annotations
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from app.core.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.models.finance.bill_invoice import Invoice
    from backend.app.models.management.purchase import PurchaseRequest, Order
    from backend.app.models.operation.stock import Invotory, StockMovement
    from app.models.finance.cash import CashAccount, CashAdjustement, CashTransaction
    from app.models.operation.product import PriceHistory
    from backend.app.models.management.sale import Sale


# Represente a point of sale
class Area(Base):
    __tablename__ = "area"
    id = Column(Integer, primary_key=True, index=True)
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
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    area_id: Mapped[int] = mapped_column(ForeignKey("area.id"), nullable=False)

    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    adress: Mapped[str | None] = mapped_column(String(255))

    # the Area where employee is affiliate
    area = relationship("Area", back_populates="employee")
    # optional one-to-one relationship with user
    user: Mapped[Optional["User"]] = relationship(back_populates="employee", uselist=False)
    purchase_initiated: Mapped[List[PurchaseRequest]] = relationship(
        back_populates="initiated_by",
        foreign_keys="PurchaseRequest.initiated_by_id",
        lazy="joined",
    )
    invoice_initiated: Mapped[Optional[List[Invoice]]] = relationship(
        back_populates="initiated_by",
        foreign_keys="Invoice.initiated_by_id",
        lazy="joined",
    )
    stock_movement_initiated: Mapped[Optional[List["StockMovement"]]] = relationship(
        back_populates="initiated_by", foreign_keys="StockMovement.initiated_by_id"
    )
    invotory_problem_investigated: Mapped[Optional[List["Invotory"]]] = relationship(
        back_populates="investigator", foreign_keys="Invotory.investigator_id"
    )


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone_number: Mapped[str | None] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(40))
    is_active: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_owner: Mapped[bool] = mapped_column(default=False)
    is_password_reinitialized: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    # To log the user's actions
    log = relationship("Log", back_populates="user")

    employee_id: Mapped[int | None] = mapped_column(ForeignKey("employee.id"), unique=True)
    employee: Mapped[Optional["Employee"]] = relationship(back_populates="user", uselist=False)
    owned_areas = relationship("Area", secondary="area_owners", back_populates="owners")

    adjustements_done: Mapped[Optional[CashAdjustement]] = relationship(
        back_populates="performed_by",
        foreign_keys="CashAdjustement.performed_by_id",
        lazy="joined",
    )

    transaction_created: Mapped[Optional[List["CashTransaction"]]] = relationship(
        back_populates="created_by",
        foreign_keys="CashTransaction.created_by_id",
        lazy="joined",
    )
    transaction_updated: Mapped[Optional[List["CashTransaction"]]] = relationship(
        back_populates="updated_by",
        foreign_keys="CashTransaction.updated_by_id",
        lazy="joined",
    )

    stock_movement_created: Mapped[Optional[List["StockMovement"]]] = relationship(
        back_populates="created_by",
        foreign_keys="StockMovement.created_by_id",
        lazy="joined",
    )
    stock_movement_updated: Mapped[Optional[List["StockMovement"]]] = relationship(
        back_populates="updated_by",
        foreign_keys="StockMovement.updated_by_id",
        lazy="joined",
    )

    purchase_created: Mapped[Optional[List[PurchaseRequest]]] = relationship(
        back_populates="created_by",
        foreign_keys="PurchaseRequest.created_by_id",
        lazy="joined",
    )
    purchase_updated: Mapped[Optional[List[PurchaseRequest]]] = relationship(
        back_populates="updated_by",
        foreign_keys="PurchaseRequest.updated_by_id",
        lazy="joined",
    )

    order_created: Mapped[Optional[List[Order]]] = relationship(
        back_populates="created_by", foreign_keys="Order.created_by_id", lazy="joined"
    )
    order_updated: Mapped[Optional[List[Order]]] = relationship(
        back_populates="updated_by", foreign_keys="Order.updated_by_id", lazy="joined"
    )

    sale_created: Mapped[Optional[List[Sale]]] = relationship(
        back_populates="created_by", foreign_keys="Sale.created_by_id", lazy="joined"
    )
    sale_updated: Mapped[Optional[List[Sale]]] = relationship(
        back_populates="updated_by", foreign_keys="Sale.updated_by_id", lazy="joined"
    )

    invoice_created: Mapped[Optional[List[Invoice]]] = relationship(
        back_populates="created_by", foreign_keys="Invoice.created_by_id", lazy="joined"
    )
    invoice_updated: Mapped[Optional[List[Invoice]]] = relationship(
        back_populates="updated_by", foreign_keys="Invoice.updated_by_id", lazy="joined"
    )

    price_history: Mapped[Optional[List["PriceHistory"]]] = relationship(
        back_populates="created_by",
        foreign_keys="PriceHistory.created_by_id",
        lazy="joined",
    )
    # Optionnal relationship
    # register_id : Mapped[int | None] = mapped_column(ForeignKey("cash_account.id"))
    cash_register: Mapped[Optional["CashAccount"]] = relationship(back_populates="user")

    # role assigned for user (one or more role). ex : manager, account, saler, logistician,..
    roles: Mapped[List["Role"]] = relationship(secondary="user_roles", back_populates="users")


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)  # name can be : manager, accountant, saler, storekeeper...
    description = Column(String(255))
    users = relationship("User", secondary="user_roles", back_populates="roles")
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="roles")


# Association table
user_role = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
)

# Association table between user and area
# user (if his owner can be have one-or-more area)
area_owners = Table(
    "area_owners",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("area_id", Integer, ForeignKey("area.id"), primary_key=True),
)
