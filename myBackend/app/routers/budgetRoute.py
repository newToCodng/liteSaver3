from fastapi import APIRouter, Depends, HTTPException
from app.models.budgetModel import BudgetCreate, BudgetOut
from app.services.budgetService import create_budget, get_user_budgets
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/budget", tags=["Budget"])


@router.post("/post_budgets", response_model=dict)
async def post_budget_route(
    budget: BudgetCreate,
    user_id: int = Depends(get_current_user)
):
    try:
        return await create_budget(user_id, budget)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_budgets", response_model=list[BudgetOut])
async def get_budgets_route(user_id: int = Depends(get_current_user)):
    try:
        return await get_user_budgets(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
