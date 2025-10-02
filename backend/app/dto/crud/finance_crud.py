from datetime import datetime
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.models.models import CashTransaction, TransactionDirection, TransactionState


class FinanceManager:
    """Finance Manager for handling financial transactions and cash register operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    """Management of cash register"""

    # Get all transactions for a specific cash register on a given date
    # This function retrieves all transactions for a specific cash register on a given date.
    # It filters the transactions based on the cash register ID and the transaction date.
    # The date is expected to be in the format of datetime.
    async def get_cash_register_transactions_by_date(self, cash_register_id: uuid.UUID, dateof: datetime):
        """Get all transactions for a specific cash register on a given date"""
        # Execute the query and return the results
        # The result is a list of CashTransaction objects for the specified cash register and date.
        # If no transactions are found, an empty list is returned.
        statement = select(CashTransaction).filter(
            CashTransaction.cash_register_id == cash_register_id, CashTransaction.dateOf == dateof
        )
        result = await self.db.execute(statement)
        return result.scalars().all()

    # Get the theoretical amount of cash in the register for a given date
    # This is the sum of all valid transactions (in and out) for that date
    async def calculate_theoretical_amount(self, cash_register_id: uuid.UUID, dateof: datetime):
        """Get the theoretical amount of cash in the register for a given date"""
        total = 0
        for trans in await self.get_cash_register_transactions_by_date(
            cash_register_id=cash_register_id, dateof=dateof
        ):
            if trans.is_valide and trans.cash_in:  # type: ignore
                total += trans.total_amount if trans.details else 0
            elif trans.is_valide and not trans.cash_in:  # type: ignore
                total -= trans.total_amount if trans.details else 0
        return total

    # This function counts the number of transactions for a specific cash register on a given date.
    # It filters the transactions based on the cash register ID, transaction validity, and transaction direction
    # This funtion return a objet contain the number of valid in, out and annuled transactions.
    # The date is expected to be in the format of datetime.
    async def count_transactions(self, cash_register_id: uuid.UUID, dateof: datetime):
        total_in_stmt = select(func.count(CashTransaction.id)).filter(
            CashTransaction.cash_register_id == cash_register_id,
            CashTransaction.status == TransactionState.COMPLETED,
            CashTransaction.direction == TransactionDirection.IN,
            CashTransaction.dateOf == dateof,
        )
        total_out_stmt = select(func.count(CashTransaction.id)).filter(
            CashTransaction.cash_register_id == cash_register_id,
            CashTransaction.status == TransactionState.COMPLETED,
            CashTransaction.direction == TransactionDirection.OUT,
            CashTransaction.dateOf == dateof,
        )
        total_annuled_stmt = select(func.count(CashTransaction.id)).filter(
            CashTransaction.cash_register_id == cash_register_id,
            CashTransaction.status == TransactionState.CANCELED,
            CashTransaction.dateOf == dateof,
        )
        total_in = (await self.db.execute(total_in_stmt)).scalar_one()
        total_out = (await self.db.execute(total_out_stmt)).scalar_one()
        total_annuled = (await self.db.execute(total_annuled_stmt)).scalar_one()
        return {"in": total_in, "out": total_out, "canceled": total_annuled}

    """End of Management of cash register"""

    """Management of cash transaction"""
    # def create_cash_transaction(session : Session, )

    """End of management of cash transaction"""
