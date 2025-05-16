from fastapi import Depends, HTTPException, APIRouter
from app.models.accountModel import Account
from app.services.accountService import create_account as create_account_service, AccountAlreadyExists, get_accounts, \
 get_account_type, DatabaseError
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/create_account")
async def create_account_route(account: Account, user_id: int = Depends(get_current_user)):
    try:
        return await create_account_service(user_id, account)
    except AccountAlreadyExists as ae:
        raise HTTPException(status_code=400, detail=str(ae))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.get("/get_accounts")
async def get_account_route(user_id: int = Depends(get_current_user)):
    try:
        return await get_accounts(user_id)
    except DatabaseError as ae:
        raise HTTPException(status_code=400, detail=str(ae))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.get("/get_account_type")
async def get_account_type_route(user_id: int = Depends(get_current_user)):
    return await get_account_type()
