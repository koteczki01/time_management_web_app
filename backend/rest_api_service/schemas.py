from datetime import datetime
from pydantic import EmailStr, BaseModel


class UserRegisterResponse(BaseModel):
    user_id: int
    birthday: datetime
    last_login: datetime
    username: str
    email: EmailStr
    created_at: datetime
    update_date: datetime
    is_active: bool


class UserLoginResponse(BaseModel):
    user_id: int
    birthday: datetime
    last_login: datetime
    username: str
    email: EmailStr
    created_at: datetime
    update_date: datetime
    is_active: bool


class UserLoginSchema(BaseModel):
    username : str
    password_hash : str


class UserRegisterSchema(BaseModel):
    username : str
    password : str
    email : EmailStr
    birthday : datetime

class ErrorOccured(BaseModel):
    message: str
