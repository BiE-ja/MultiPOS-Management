from datetime import datetime
from sqlalchemy import func
from backend.app.models.finance import CashTransaction, TransactionDirection, TransactionState
from sqlalchemy.orm import Session

"""Management of cash register"""
# Get all transactions for a specific cash register on a given date
# This function retrieves all transactions for a specific cash register on a given date.
# It filters the transactions based on the cash register ID and the transaction date.
# The date is expected to be in the format of datetime.
def get_cash_register_transactions_by_date(db: Session, cash_register_id: int, dateof : datetime):
     """Get all transactions for a specific cash register on a given date"""
     return db.query(CashTransaction).filter(
          CashTransaction.cash_register_id == cash_register_id,
          CashTransaction.transac_date == dateof
     ).all()

# Get the theoretical amount of cash in the register for a given date
# This is the sum of all valid transactions (in and out) for that date
def calculate_theoretical_amount(db : Session, cash_register_id: int, dateof : datetime):
    """Get the theoretical amount of cash in the register for a given date"""
    total = 0
    for trans in get_cash_register_transactions_by_date(db, cash_register_id = cash_register_id, dateof = dateof):
        if trans.is_valide and trans.cash_in: # type: ignore
            total += trans.total_amount if trans.details else 0
        elif trans.is_valide and not trans.cash_in :  # type: ignore
            total -= trans.total_amount if trans.details else 0
    return total


# This function counts the number of transactions for a specific cash register on a given date.
# It filters the transactions based on the cash register ID, transaction validity, and transaction direction
# This funtion return a objet contain the number of valid in, out and annuled transactions.
# The date is expected to be in the format of datetime.
def count_transactions(db : Session, cash_register_id:int, dateof: datetime):
    total_in = db.query(func.count(CashTransaction.id)).filter(
        CashTransaction.cash_register_id == cash_register_id,
        CashTransaction.status == TransactionState.COMPLETED,
        CashTransaction.direction == TransactionDirection.IN,
        CashTransaction.dateOf == dateof
    )
    total_out = db.query(func.count(CashTransaction.id)).filter(
        CashTransaction.cash_register_id == cash_register_id,
        CashTransaction.status == TransactionState.COMPLETED,
        CashTransaction.direction == TransactionDirection.OUT,
        CashTransaction.dateOf == dateof
    )
    total_annuled = db.query(func.count(CashTransaction.id)).filter(
        CashTransaction.status == TransactionState.CANCELED,
        CashTransaction.dateOf == dateof
    )
    return {
        "in" : total_in,
        "out": total_out,
        "canceled" : total_annuled
    }
               
        
"""End of Management of cash register"""

"""Management of cash transaction"""
#def create_cash_transaction(session : Session, )





"""End of management of cash transaction"""