from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from app.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from backend.app.models.finance import CashAccount, CashTransaction

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    area_id = Column(Integer, ForeignKey("area.id"),nullable=False)
    
    area = relationship("Area", back_populates="customer")
    sale = relationship("Sale", back_populates="customer")

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
    employee = relationship("Employee", bakc_populates="user", cascade="all, delete-orphan")
    area= relationship("Area", back_populates="user")
    adjustement_done = relationship("CashAdjustement", back_populates="user")
    transaction_created : Mapped[List["CashTransaction"]] = relationship(back_populates="created_by", foreign_keys="CashTransaction.created_by_id")
    transaction_cancelled : Mapped[List["CashTransaction"]] = relationship(back_populates="cancelled_by", foreign_keys="CashTransaction.cancelled_by_id")
    # Optionnal relationship
    register_id : Mapped[int | None] = mapped_column(ForeignKey("cash_account.id"))
    cash_account : Mapped[Optional["CashAccount"]] = relationship(back_populates="user")
# Association table
employee_role = Table(
    "employee_role",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employee.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
)

class Employee(Base):
    __tablename__="employee"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    
    # the Area where employee is affiliate
    area = relationship("Area", back_populates="employee")
    user = relationship("User", back_populates="employee")
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
