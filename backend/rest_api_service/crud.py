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