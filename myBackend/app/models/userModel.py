from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional
from datetime import date


class UserRegister(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
    first_name: str
    last_name: str
    dob: date
    phone_number: Optional[Annotated[str, Field(min_length=11, max_length=11)]]


class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class UserOut(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr

