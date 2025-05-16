from fastapi import APIRouter, Depends, HTTPException
from app.services.currencyService import get_currency, DatabaseError
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/currency", tags=["Currency"])


@router.get("/currencies")
async def get_currency_route(user_id: int = Depends(get_current_user)):
    try:
        return await get_currency()
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
