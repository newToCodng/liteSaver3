from pydantic import BaseModel, condecimal, Field
from datetime import date


class BudgetCreate(BaseModel):
    category_id: int
    budget_amount: condecimal(gt=0, max_digits=12, decimal_places=2)
    start_date: date
    end_date: date


class BudgetOut(BudgetCreate):
    budget_id: int
    current_amount: condecimal(ge=0, max_digits=12, decimal_places=2)
    progress_percentage: float
    is_active: bool
