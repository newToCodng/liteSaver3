from pydantic import BaseModel
from enum import Enum


class AccountType(str, Enum):
    CASH = 'Cash'
    BANK = 'Bank'
    CREDIT_CARD = 'Credit Card'
    INVESTMENT = 'Investment'
    LOAN = 'Loan'


class Account(BaseModel):
    name: str
    balance: float = 0  # user can set balance if they want to
    currency_id: int
    account_type: AccountType
