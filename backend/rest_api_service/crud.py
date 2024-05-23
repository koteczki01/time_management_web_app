import datetime
import logging
from typing import Type
import models
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import DBUser
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


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


async def create_friend_request(db: Session, sender_id: int, recipient_id: int, friendship_status="pending") -> models.DBUserFriendship | dict:
    try:
        friendship = models.DBUserFriendship(user1_id=sender_id, user2_id=recipient_id, friendship_status=friendship_status)

        db.add(friendship)
        db.commit()

        return friendship
    except IntegrityError as e:
        return {'error': repr(e)}


async def get_friend_request(db: Session, sender_id: int, recipient_id: int) -> models.DBUserFriendship | None:
    friendship = db.query(models.DBUserFriendship).filter(and_(models.DBUserFriendship.user1_id == sender_id, models.DBUserFriendship.user2_id == recipient_id)).first()

    return friendship


async def alter_friend_request(db: Session, sender_id: int, recipient_id: int, action: str) -> models.DBUserFriendship | dict:
    friendship = await get_friend_request(db, sender_id=sender_id, recipient_id=recipient_id)

    if friendship:
        if friendship.friendship_status in ['accepted', 'rejected']:
            return {"error": f"Friendship already {friendship.friendship_status}"}

        friendship.friendship_status = action
        friendship.action_time = datetime.datetime.now()

        db.commit()
        db.refresh(friendship)

        reversed_friendship = await get_friend_request(db, sender_id=recipient_id, recipient_id=sender_id)
        if reversed_friendship is None:
            # create entry for recipient -> sender
            await create_friend_request(db, sender_id=recipient_id, recipient_id=sender_id, friendship_status=action)
        else:
            reversed_friendship.friendship_status = action
            reversed_friendship.action_time = datetime.datetime.now()

            db.commit()
            db.refresh(reversed_friendship)

        return friendship
    return {"error": "Friend request not found"}
