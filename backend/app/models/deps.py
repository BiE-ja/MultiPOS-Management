from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from app.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from backend.app.models.finance.cash import CashAccount, CashAdjustement, CashTransaction
from backend.app.models.operation.bill_invoice import Invoice
from backend.app.models.operation.purchase import PurchaseRequest
from backend.app.models.operation.stock import StockMovement


# Represente a point of sale
class Area (Base):
    __tablename__="area"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    location = Column(String(255))
    owner = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="area")
    employee = relationship("Employee", back_populates="area", cascade = "all, delete-orphan")
    customer = relationship("Customer", back_populates="area", cascade = "all, delete-orphan")
    product = relationship("Product", back_populates="area", cascade = "all, delete-orphan")
    purchase = relationship("Purchase", back_populates="area", cascade="all, delete-orphan")
    sale = relationship("Sale", back_populates="area", cascade="all, delete-orphan")
    supplier = relationship("Supplier", back_populates="area", cascade="all, delete-orphan")
    cash_register = relationship("cash_register", back_populates="area", cascade="all, delete-orphan")
    stock = relationship("StockMovement", back_populates="area", cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates = "area", cascade="all, delete-orphan")

# Association table
employee_role = Table(
    "employee_role",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employee.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
)

class Employee(Base):
    __tablename__="employee"
    id : Mapped[int]= mapped_column(primary_key=True, index=True)
    user_id : Mapped[int| None]= mapped_column(ForeignKey("user.id"))
    area_id : Mapped[int]= mapped_column(ForeignKey("area.id"), nullable=False)
    
    # the Area where employee is affiliate
    area = relationship("Area", back_populates="employee")
    user = relationship("User", back_populates="employee",uselist=False, cascade="all, delete-orphan")
    purchase_initiated : Mapped[List[PurchaseRequest]] = relationship(back_populates="employee", foreign_keys="PurchaseRequest.initiated_by_id", lazy="joined")
    # role assigned for employee (one or more role). ex : manager, account, saler, logistician,..
    roles = relationship(
        "Role",
        secondary= employee_role,
        back_populates="employees"
    )

class Role(Base):
    __tablename__="role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # name can be : manager, accountant, saler, storekeeper...
    employee = relationship(
        "Role",
        secondary= employee_role,
        back_populates="employees"
    )


class User(Base):
    __tablename__="user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashed_password= Column(String(40))
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)

    # To log the user's actions
    log = relationship("Log", back_populates="user")
    employee = relationship("Employee", bakc_populates="user")
    area= relationship("Area", back_populates="user")
    adjustement_done : Mapped[Optional[CashAdjustement]] = relationship(back_populates="user")
    
    transaction_created : Mapped[Optional[List["CashTransaction"]]] = relationship(back_populates="created_by", foreign_keys="CashTransaction.created_by_id")
    transaction_cancelled : Mapped[Optional[List["CashTransaction"]]] = relationship(back_populates="cancelled_by", foreign_keys="CashTransaction.cancelled_by_id")
    
    stock_movement_initiated : Mapped[Optional[List["StockMovement"]]] = relationship(back_populates="created_by", foreign_keys="StockMovement.initiated_by_id")
    stock_movement_cancelled : Mapped[Optional[List["StockMovement"]]] = relationship(back_populates="cancelled_by", foreign_keys="StockMovement.cancelled_by_id")
    
    purchase_created : Mapped[Optional[List[PurchaseRequest]]] = relationship(back_populates="created_by", foreign_keys="PurchaseRequest.created_by_id", lazy="joined")
    purchase_updated : Mapped[Optional[List[PurchaseRequest]]] = relationship(back_populates="updated_by", foreign_keys="PurchaseRequest.updated_by_id", lazy="joined")
    
    invoice_created :Mapped[Optional[List[Invoice]]] = relationship(back_populates="created_by", foreign_keys="Invoice.created_by_id", lazy="joined")
    invoice_updated : Mapped[Optional[List[Invoice]]] = relationship(back_populates="updated_by", foreign_keys="Invoice.updated_by_id", lazy="joined")
    
    # Optionnal relationship
    register_id : Mapped[int | None] = mapped_column(ForeignKey("cash_account.id"))
    cash_account : Mapped[Optional["CashAccount"]] = relationship(back_populates="user")

class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, index=True)
    dateAction = date = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    action = Column(String)

    user = relationship("User", back_populates="Log")