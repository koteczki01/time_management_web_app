from typing import Type
import models
from sqlalchemy.orm import Session, joinedload
from models import DBUser, DBUserFriendship
from datetime import date, datetime


async def get_all_users(db: Session) -> list[Type[DBUser]] | None:
    users = db.query(models.DBUser).all()

    return users



 
async def get_user_by_id(db: Session, user_id: int) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUser.user_id == user_id).first()
    return user

async def get_user_by_username(db: Session, username: str) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUser.username == username).first()
    return user

async def get_all_events_by_user_id(db: Session, user_id: int) -> models.DBUser | None:
    user = db.query(models.DBEvent).filter(models.DBEvent.created_by == user_id).first()
    return user

async def get_all_friends_by_user_id(db: Session, user_id: int) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUserFriendship.user1_id == user_id).first()
    if user:
        return user
    return None

async def get_all_active_users(db: Session) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUser.is_active == True).all()
    return user

async def create_user(db: Session, username: str, email: str, password_hash: str, birthday: date, is_active: bool = True):
    new_user = DBUser(
        username=username,
        email=email,
        password_hash=password_hash,
        birthday=birthday,
        created_at=date.today(),
        last_login=date.today(),
        update_date=date.today(),
        is_active=is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user_birthday(db: Session, user_id: int, new_birthday: date):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if user:
        user.birthday = new_birthday
        user.update_date = date.today()
        db.commit()
        db.refresh(user)
        return user
    else:
        return None

async def change_user_password(db: Session, user_id: int, new_password_hash: str):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if user:
        user.password_hash = new_password_hash
        user.update_date = date.today()
        db.commit()
        db.refresh(user)
        return user
    else:
        return None
    
async def change_user_email(db: Session, user_id: int, new_email: str):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if user:
        user.email = new_email
        user.update_date = date.today()
        db.commit()
        db.refresh(user)
        return user
    else:
        return None
    
async def change_user_username(db: Session, user_id: int, new_username: str):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if user:
        user.username = new_username
        user.update_date = date.today()
        db.commit()
        db.refresh(user)
        return user
    else:
        return None
       

async def update_user_last_login(db: Session, user_id: int):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if user:
        now = datetime.now().replace(microsecond=0)
        user.last_login = now
        user.update_date = now
        db.commit()
        db.refresh(user)
        return user
    else:
        return None


async def get_all_categories(db: Session) -> list[Type[models.DBCategory]] | None:
    categories = db.query(models.DBCategory).all()

    return categories


async def get_all_events(db: Session) -> list[Type[models.DBEvent]] | None:
    events = db.query(models.DBEvent).all()

    return events


async def get_all_participants(db: Session) -> list[Type[models.DBEventParticipants]] | None:
    participants = db.query(models.DBEventParticipants).all()

    return participants
