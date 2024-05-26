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
    username: str
    password_hash: str


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    birthday: datetime


class ErrorOccured(BaseModel):
    message: str


class Friendship(BaseModel):
    friendship_id: int
    user1_id: int
    user2_id: int
    friendship_status: str


class UserSchema(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    birthday: datetime
    created_at: datetime
    last_login: datetime
    update_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None