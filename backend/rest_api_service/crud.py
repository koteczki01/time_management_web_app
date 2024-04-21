from typing import Type
import models
from sqlalchemy.orm import Session, joinedload
from models import DBUser, DBUserFriendship
from datetime import date


async def get_all_users(db: Session) -> list[Type[DBUser]] | None:
    users = db.query(models.DBUser).all()

    return users



 
async def get_user_by_id(db: Session, user_id: int) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUser.user_id == user_id).first()
    print(user)
    
    return user

async def get_user_by_username(db: Session, username: str) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUser.username == username).first()
    print(user)
    
    return user

async def get_all_events_by_user_id(db: Session, user_id: int) -> models.DBUser | None:
    user = db.query(models.DBUser).options(joinedload(models.DBUser.events_created)).filter(models.DBUser.user_id == user_id).first()
    return user


async def get_all_friends_by_user_id(db: Session, user_id: int) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUser.user_id == user_id).first()
    if user:
        return user.friends
    return None

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

async def delete_user(db: Session, user_id: int) -> bool:
    user = await get_user_by_id(db, user_id)
    if user:
        # Usuń rekordy z tabeli DBUserFriendship powiązane z użytkownikiem
        db.query(DBUserFriendship).filter(
            (DBUserFriendship.user1_id == user_id) | (DBUserFriendship.user2_id == user_id)
        ).delete(synchronize_session=False)
        # Usuń użytkownika
        db.delete(user)
        db.commit()
        return True
    return False








async def get_all_categories(db: Session) -> list[Type[models.DBCategory]] | None:
    categories = db.query(models.DBCategory).all()

    return categories


async def get_all_events(db: Session) -> list[Type[models.DBEvent]] | None:
    events = db.query(models.DBEvent).all()

    return events


async def get_all_participants(db: Session) -> list[Type[models.DBEventParticipants]] | None:
    participants = db.query(models.DBEventParticipants).all()

    return participants
