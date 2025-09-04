from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum as pyEnum
from typing import  List, Optional,TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Numeric, Enum as sqlEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

if TYPE_CHECKING:
    

    from backend.app.models.finance.cash import CashTransaction
    from backend.app.models.finance.bill_invoice import Invoice
    from backend.app.models.management.sale import Sale
class PaymentMethod(pyEnum):
    CARD = "card"
    CHECK = "check"
    CASH = "cash"
    WIRE = "wire"

class TransactionType (pyEnum):
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
    # vente validé mais pas encore payé (cas où c'est un autre employé qui saisie la vente et le paiement se fait à la caisse)
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
    __tablename__="payments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reference : Mapped[str | None]= mapped_column()
    amount: Mapped[float] = mapped_column(Numeric(18, 2))  # Amount of the payment
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    method : Mapped["PaymentMethod"] = mapped_column(sqlEnum(PaymentMethod), nullable=False) # ex : cash, card, etc.
    state : Mapped["TransactionState"] = mapped_column(sqlEnum(TransactionState), nullable = False)
    direction : Mapped["TransactionType"] = mapped_column(sqlEnum(TransactionType), nullable = False)
    sale_id : Mapped[int| None] = mapped_column(ForeignKey("sale.id"), nullable=False)  
    invoice_id : Mapped[int| None] = mapped_column(ForeignKey("invoice.id"), nullable=False)   
    # Optional FK if the payment is linked to a cash transaction
    # If the payment is not linked to a cash transaction, this can be None
    cash_transac_id: Mapped[int | None] = mapped_column(ForeignKey("cash_transaction.id"), nullable=True)

    cash_transaction: Mapped[Optional["CashTransaction"]] = relationship(back_populates="payments", uselist=False, lazy="joined")
    # Reverse relation from sale, payment
    sale : Mapped[Optional["Sale"]]= relationship(back_populates="payments", uselist=False, lazy="joined")
    invoice : Mapped[Optional[List["Invoice"]]]= relationship(back_populates="payments", uselist=False, lazy="joined")
    

