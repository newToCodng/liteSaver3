from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.token import decode_access_token
from fastapi import HTTPException, status, Depends


oauth2_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    payload = decode_access_token(token.credentials)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: user_id is missing"
        )
    return user_id
