import datetime
from pydantic import EmailStr, BaseModel


class UserRegisterResponse(BaseModel):
    user_id: int
    birthday: datetime.datetime
    last_login: datetime.datetime
    username: str
    email: EmailStr
    created_at: datetime.datetime
    update_date: datetime.datetime
    is_active: bool


class UserLoginResponse(BaseModel):
    user_id: int
    birthday: datetime.datetime
    last_login: datetime.datetime
    username: str
    email: EmailStr
    created_at: datetime.datetime
    update_date: datetime.datetime
    is_active: bool


class UserLoginSchema(BaseModel):
    username : str
    password_hash : str


class UserRegisterSchema(BaseModel):
    username : str
    password : str
    email : EmailStr
    birthday : datetime.datetime

class ErrorOccured(BaseModel):
    message: str
