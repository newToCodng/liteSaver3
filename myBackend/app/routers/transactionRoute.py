from fastapi import APIRouter, Depends, HTTPException
from app.models.transactionModel import TransactionCreate
from app.services.transactionService import create_transaction
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/add_transactions")
async def add_transaction(
    transaction: TransactionCreate,
    user_id: int = Depends(get_current_user)
):
    try:
        return await create_transaction(transaction, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_transactions")
async def get_transactions(user_id: int = Depends(get_current_user)):
    return await get_transactions(user_id)

