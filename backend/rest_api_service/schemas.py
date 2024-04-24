import datetime
from pydantic import EmailStr, BaseModel
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import Mapped



class UserLoginSchema(BaseModel):
  username : str
  password_hash : str


class UserRegisterSchema(BaseModel):
  username : str
  password : str
  email : EmailStr
  birthday : datetime.datetime
