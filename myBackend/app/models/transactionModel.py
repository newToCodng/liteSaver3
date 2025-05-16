from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class TransactionCreate(BaseModel):
    account_id: int
    category_id: int
    currency_id: int
    amount: Decimal
    description: str = ""


