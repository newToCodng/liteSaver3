from fastapi import APIRouter, HTTPException, Depends
from app.models.userModel import UserRegister, UserLogin, UserOut
from app.services.userService import create_user, authenticate_user, get_user_profile, UserNotFound, UserAlreadyExists, InvalidLoginDetails, DatabaseError
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/ping")
def route_health():
    return {"message": "Users route is active ✅"}


@router.post("/register")
async def register_user(user: UserRegister):
    try:
        user_id = await create_user(user)
        return {"message": "User created successfully", "user_id": user_id}
    except UserAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/login")
async def login_user(user: UserLogin):
    try:
        return await authenticate_user(user)
    except InvalidLoginDetails as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=UserOut)
async def read_current_user(user_id: int = Depends(get_current_user)):
    try:
        user_profile = await get_user_profile(user_id)
        return user_profile
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        # For unexpected errors, log if needed
        raise HTTPException(status_code=500, detail="Internal server error")




