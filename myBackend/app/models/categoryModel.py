from pydantic import BaseModel
from enum import Enum


class CategoryType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'


class CategoryIn(BaseModel):
    name: str
    category_type: CategoryType


class CategoryOut(BaseModel):
    category_id: int
    name: str
    category_type: CategoryType
