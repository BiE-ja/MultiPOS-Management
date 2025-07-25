from datetime import datetime, timezone
from enum import Enum as pyEnum
from typing import List, Optional
from sqlalchemy import Column, DateTime, Enum as sqlEnum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates
from app.database import Base
from backend.app.models.area import Area
from backend.app.models.people import User
from backend.app.models.sale import Sale

# Represent a payment made for a sale (can be cash, card, etc.)
class Payment(Base):
    __tablename__="payments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reference : Mapped[str | None]= mapped_column()
    amount: Mapped[float] = mapped_column(Numeric(18, 2))  # Amount of the payment
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    method : Mapped[str] = mapped_column(String(50)) # ex : cash, card, etc.
    sale_id : Mapped[int] = mapped_column(ForeignKey("sale.id"), nullable=False)
    # Optional FK if the payment is linked to a cash transaction
    # If the payment is not linked to a cash transaction, this can be None
    cash_transac_id: Mapped[int | None] = mapped_column(ForeignKey("cash_transaction.id"), nullable=True)

    cash_transaction: Mapped["CashTransaction"] = relationship(back_populates="payment", uselist=False, lazy="joined", cascade="all, delete-orphan")
    # Reverse relation from sale
    sale : Mapped["Sale"]= relationship(back_populates="payment", uselist=False, lazy="joined")

# This is used to indicate the direction of the transaction
class TransactionDirection(str, pyEnum):
    IN = "in"
    OUT = "out"

# This is used to indicate the type of operation performed in the transaction
class TransactionPurpose(str, pyEnum):
    SALE_PAYMENT = "sale_payment" # IN
    SUPPLY = "supply" # OUT
    CORRECTION = "correction" # IN or OUT
    BANK_TRANSFERT = "bank_transfert" # OUT
    MISC_EXPENSE = "misc_expense" # OUT

# This is used to indicate the status of the transaction
# It can be used to track if the transaction is pending, completed, or failed
class TransactionState(str, pyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

# Represent an actual movement of money in or out of the cash register
# This can be a payment for a sale, a cash deposit, or a cash withdrawal"""
class CashTransaction(Base):
    """Represent an actual movement of money in or out of the cash register\n
    This can be a payment for a sale, a cash deposit, or a cash withdrawal
    """
    __tablename__="cash_transaction"
    id : Mapped[int]= mapped_column(primary_key=True, index = True)
    direction : Mapped[TransactionDirection] = mapped_column(sqlEnum(TransactionDirection), nullable=False)
    operation : Mapped[TransactionPurpose] = mapped_column(sqlEnum(TransactionPurpose), nullable=False)
    status : Mapped[TransactionState] = mapped_column(sqlEnum(TransactionState), default=TransactionState.PENDING, nullable=False)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    # info of annulation
    cancellation_reason : Mapped[str | None] = mapped_column(String(255))  # Reason for cancellation or correction
    cancellet_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # When the transaction was canceled
    cancelled_by_id : Mapped [int | None]= mapped_column(ForeignKey("user.id"))  # Nullable if not canceled
    
    register_id: Mapped[int] = mapped_column(Integer, ForeignKey("cash_account.id"), nullable=False)
    payment_ref : Mapped[str | None ]= mapped_column()
    # Date of the transaction
    dateOf : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    register : Mapped["CashAccount"] = relationship(back_populates="CashAccount", lazy="joined", uselist=False)
    details  : Mapped[List["CashTransactionLine"]] = relationship(back_populates = "cash_transac", cascade = "all, delete-orphan")
    # relationship to the user who created the transaction
    created_by : Mapped["User"] = relationship(back_populates="transaction_created", foreign_keys="CashTransaction.created_by_id", lazy="joined")
    # relationship to the user who canceled the transaction 
    cancelled_by : Mapped["User"] = relationship(back_populates="transaction_cancelled", foreign_keys="CashTransaction.cancelled_by_id", lazy="joined")
    # relationship to the payment if it exists
    payment : Mapped[Optional["Payment"]] = relationship(back_populates="cash_transaction", uselist=False, lazy="joined")
   
    # --- Useful helper ---
    @property
    def is_valid(self):
        """ Check if the transaction is valid (not canceled or failed) """
        return self.status == TransactionState.COMPLETED
    @property
    def cancel(self):
        """ Cancel the transaction (does not delete it) """
        """Cancels the transaction if it is valid."""
        if not self.is_valid:
            raise ValueError("This transaction is already canceled.")
        if self.operation == TransactionPurpose.SALE_PAYMENT:
            raise ValueError("Sale payments cannot be canceled directly.")
        self.state = TransactionState.CANCELED
    @property
    def total_amount(self):
        """ get the amount of transaction"""
        """Amount of the transaction (can be positive or negative depending on the direction)"""
        amount = sum(details.value for details in self.details) 
        if self.direction == TransactionDirection.OUT:
            amount = amount * (-1)
        return amount
    
    @validates("operation", "direction")
    def validate_coherance(self, key, value): # type: ignore 
        """ Ensure operation matches direction logic"""
        operation = value if key == "operation" else self.operation  # type: ignore
        direction = value if key == "direction" else self.direction # type: ignore

        # Only validate if both are already set
        if operation and direction:
            in_operations = {TransactionPurpose.SALE_PAYMENT, TransactionPurpose.SUPPLY} 
            out_operations = {TransactionPurpose.BANK_TRANSFERT, TransactionPurpose.MISC_EXPENSE}
            # Correction is flexible
            
            if direction == TransactionDirection.IN and operation in out_operations:
                raise ValueError(f"Operation ' {operation} ' cannot be used with IN direction.")
            elif direction == TransactionDirection.OUT and operation in in_operations:
                raise ValueError(f"Operatiion '{operation}' cannot be used with OUT direction.")
        return value # type: ignore

# e.g : 20.000 * 5
class CashTransactionLine(Base):
    __tablename__="transaction_details"
    id : Mapped[int] =mapped_column(primary_key=True, index = True)
    transac_id : Mapped[int] =mapped_column(ForeignKey("cash_transaction.id"), nullable = False, unique= True)
    denomination_id : Mapped[int] =mapped_column(ForeignKey("denomination.id", nullable = False))
    quantity: Mapped[int] = mapped_column()

    cash_transac : Mapped[CashTransaction]= relationship(back_populates="details", uselist=False)
    denomination : Mapped["Denomination"] = relationship(back_populates="transaction_details", uselist=False)
    @property
    def value (self):
        return (self.quantity * self.denomination.value)

# This class represent a bank billet 
class Denomination(Base):
    __tablename__ = "denomination"
    id : Mapped[int] =mapped_column(primary_key=True, index = True)
    name : Mapped[str]= mapped_column(String(10), unique=True)  # e.g., "20000", "10000", etc.
    value : Mapped[float] = mapped_column(Numeric(18, 2))  # because value can be 0,20 Ar or 0,50 USD
    currency : Mapped[str] = mapped_column(String(10))
    
    adjustement : Mapped["CashAdjustementLine"] = relationship(back_populates="denomination")
    transaction : Mapped["CashTransactionLine"] = relationship(back_populates="denomination")
    def __repr__(self):
        return f"<Denomination(name={self.name}, value={self.value})>"

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

    
# Represent a signle cash account (like a bank or  cash register)
class CashAccount(Base):
    __tablename="cash_account"
    id : Mapped[int] =mapped_column(primary_key=True, index = True)
    amount_init : Mapped[float] = mapped_column(Numeric(18,2)) 
    state : Mapped[CashAccountState] = mapped_column(sqlEnum(CashAccountState), nullable=False) # state : open, closed, balanced, notBalanced, balanced_forced
    employee_id : Mapped[int] = mapped_column( ForeignKey("employee.id"))
    area_id : Mapped[int] = mapped_column(Integer, ForeignKey("area.id"))
    # amount edited by employee during balancing
    balancing_amount : Mapped[float] = mapped_column(Numeric(18,2))

    # Relationship
    adjustement : Mapped["CashAdjustement"]= relationship(back_populates="cash_register", uselist=False, cascade="all, delete-orphan")
    details : Mapped["CashAdjustementLine"] = relationship(back_populates="cash_reg", uselist=False, cascade="all, delete-orphan")
    transactions : Mapped[List["CashTransaction"]] = relationship(back_populates = "cash_register", cascade = "all, delete-orphan")
    user : Mapped["User"]= relationship(back_populates="cash_register")
    area : Mapped["Area"]= relationship(back_populates="cash_register")  

class CashAdjustement(Base):
    __tablename__ = "cash_adjustement"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    register_id : Mapped[int] = mapped_column(ForeignKey("cash_register.id"), nullable=False)
    performed_by_id : Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    typeOf : Mapped["CashAdjustementType"] = mapped_column(sqlEnum(CashAdjustementType), nullable=False) # reason for adjustment : opening, closing, correction
    dateof : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship
    cash_register : Mapped["CashAccount"] = relationship(back_populates="adjustements")
    performed_by : Mapped["User"] = relationship(back_populates="cash_adjustement")
    details: Mapped[List["CashAdjustementLine"]] = relationship(back_populates="adjustement", cascade="all, delete-orphan")
    
    @property
    def total_amount(self) -> float:
        return sum(details.value for details in self.details) 

 # e.g : 20.000 * 5
class CashAdjustementLine(Base):
    __tablename__ = "cash_details"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    adjustement_id : Mapped[int] = mapped_column(ForeignKey("cash_adjustement.id"), nullable=False)
    denomination_id : Mapped[int] = mapped_column(ForeignKey("denomination.id"), nullable=False)
    quantity : Mapped[int] = mapped_column()

    denomination : Mapped[Denomination] = relationship(back_populates="cash_details", uselist=False)
    adjustement : Mapped["CashAdjustement"] = relationship(back_populates="details")
    @property
    def value (self):
        return (self.quantity * self.denomination.value)
