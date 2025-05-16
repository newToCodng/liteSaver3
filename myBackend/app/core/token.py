import os
from jose import jwt, JWTError
from fastapi import HTTPException, status
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
token_exp_min = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE"))


# generate token payload
def create_user_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=token_exp_min))
    to_encode.update({"exp": expire})
    payload = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return payload


# decode jwt token to allow access
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )






