from fastapi import APIRouter, Depends, HTTPException
from app.models.categoryModel import CategoryIn, CategoryOut
from app.services.categoryService import create_category, DatabaseError, CategoryAlreadyExists, get_categories_service
from app.core.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/create_category")
async def create_category_route(category: CategoryIn, user_id: int = Depends(get_current_user)):
    try:
        return await create_category(user_id, category)
    except CategoryAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_category", response_model=List[CategoryOut])
async def get_categories_route(user_id: int = Depends(get_current_user)):
    try:
        return await get_categories_service(user_id)
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
