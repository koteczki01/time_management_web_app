import datetime
from typing import Type
import models
from sqlalchemy.orm import Session
from models import DBUser


async def get_all_users(db: Session) -> list[Type[DBUser]] | None:
    users = db.query(models.DBUser).all()

    return users


async def get_all_categories(db: Session) -> list[Type[models.DBCategory]] | None:
    categories = db.query(models.DBCategory).all()

    return categories


async def get_all_events(db: Session) -> list[Type[models.DBEvent]] | None:
    events = db.query(models.DBEvent).all()

    return events


async def get_all_participants(db: Session) -> list[Type[models.DBEventParticipants]] | None:
    participants = db.query(models.DBEventParticipants).all()

    return participants


async def get_user_by_id(db: Session, user_id: int) -> Type[models.DBUser] | None:
    user = db.query(models.DBUser).filter(models.user.DBUser.id == user_id).first()

    return user


async def get_user_by_username(db: Session, username: str) -> Type[models.DBUser] | None:
    user = db.query(models.DBUser).filter(models.DBUser.username == username).first()

    return user


async def create_user(db: Session, username: str, email : str, password_hash: str, birthday : datetime.datetime) -> models.DBUser | None:
    user = models.DBUser(
        username=username, 
        email=email, 
        password_hash=password_hash, 
        birthday=birthday, 
        created_at=datetime.datetime.now(), 
        last_login=datetime.datetime.now(), 
        update_date=datetime.datetime.now(), 
        is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user_last_login(db: Session, id : int) -> None:
    user = db.query(models.DBUser).filter(models.DBUser.user_id == id).first()
    if user:
        user.last_login = datetime.datetime.now()
        db.commit()
        db.refresh(user)