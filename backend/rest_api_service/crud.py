import datetime
from typing import Type
import models
from sqlalchemy.orm import Session
from models import DBUser
from sqlalchemy.orm.exc import NoResultFound


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
    try:
        user = db.query(models.DBUser).filter(models.DBUser.user_id == user_id).first()
        return user
    except NoResultFound:
        return None
    except Exception as e:
        return None


async def get_user_by_username(db: Session, username: str) -> Type[models.DBUser] | None:
    try:
        user = db.query(models.DBUser).filter(models.DBUser.username == username).first()
        return user
    except NoResultFound:
        return None
    except Exception as e:
        return None


async def create_user(db: Session, username: str, email: str, password_hash: str, birthday: datetime.datetime) -> models.DBUser | None:
    try:
        user = models.DBUser(
            username=username,
            email=email,
            password_hash=password_hash,
            birthday=birthday,
            created_at=datetime.datetime.now(),
            last_login=datetime.datetime.now(),
            update_date=datetime.datetime.now(),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()  
        return None 


async def update_user_last_login(db: Session, id : int) -> None:
    try:
        user = await get_user_by_id(db, id)
        if user:
            user.last_login = datetime.datetime.now()
            db.commit()
            db.refresh(user)
    except Exception:
        db.rollback()  
        return None

async def create_friend_request(db: Session, sender_id: int, recipient_id: int) -> DBUserFriendship:
    friendship = DBUserFriendship(user1_id=sender_id, user2_id=recipient_id, friendship_status=FriendshipStatus.pending)
    db.add(friendship)
    db.commit()
    return friendship

async def get_friend_request(db: Session, sender_id: int) -> DBUserFriendship:
    friendship = db.query(DBUserFriendship).filter(
        (DBUserFriendship.user1_id == sender_id) | (DBUserFriendship.user2_id == sender_id)
    ).filter_by(friendship_status=FriendshipStatus.pending).first()
    return friendship


