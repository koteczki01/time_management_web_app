from typing import Type

import models
from models import DBUser, DBUserFriendship
from datetime import date, datetime


from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_

 
async def get_user_by_id(db: Session, user_id: int) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUser.user_id == user_id).first()
    return user

async def get_user_by_username(db: Session, username: str) -> models.DBUser | None:
    user = db.query(models.DBUser).filter(models.DBUser.username == username).first()
    return user

async def get_all_events_by_user_id(db: Session, user_id: int) -> models.DBUser | None:
    user = db.query(models.DBEvent).filter(models.DBEvent.created_by == user_id).first()
    return user

async def get_all_friends_of_user_by_user_id(db: Session, user_id: int):

    user_alias = aliased(DBUser)

    friends1 = db.query(user_alias).join(
        DBUserFriendship,
        DBUserFriendship.user1_id == user_id
    ).filter(
        DBUserFriendship.user2_id == user_alias.user_id,
        user_alias.is_active == True
    )

    friends2 = db.query(user_alias).join(
        DBUserFriendship,
        DBUserFriendship.user2_id == user_id
    ).filter(
        DBUserFriendship.user1_id == user_alias.user_id,
        user_alias.is_active == True
    )

    active_friends = friends1.union(friends2).all()

    return active_friends

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


async def create_user(db: Session, username: str, email: str, password_hash: str,
                      birthday: datetime) -> models.DBUser | None:
    try:
        user = models.DBUser(
            username=username,
            email=email,
            password_hash=password_hash,
            birthday=birthday,
            created_at=datetime.now(),
            last_login=datetime.now(),
            update_date=datetime.now(),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        return None


async def update_user_last_login(db: Session, id: int) -> None:
    try:
        user = await get_user_by_id(db, id)
        if user:
            user.last_login = datetime.now()
            db.commit()
            db.refresh(user)
    except Exception:
        db.rollback()
        return None
    

async def change_password(db: Session, id: int, password_hash : str):
    try:
        user = await get_user_by_id(db, id)
        if user:
            user.password_hash = password_hash;
            user.update_date = date.today()
            db.commit()
            db.refresh(user)
            return user
    except Exception:
        db.rollback()
        return None


async def get_event_by_id(event_id: int, db: Session):
    return db.get(models.DBEvent, event_id)


async def get_all_events_of_user_by_user_id(user_id: int, db: Session):
    return db.query(models.DBEvent).join(models.DBEventParticipants).filter(
        models.DBEventParticipants.user_id == user_id).all()


async def get_all_events_by_creator_id(user_id: int, db: Session):
    return db.query(models.DBEvent).filter(
        models.DBEvent.created_by == user_id).all()


async def get_all_event_participants(event_id: int, db: Session):
    return db.query(models.DBUser).join(models.DBEventParticipants).filter(
        models.DBEventParticipants.event_id == event_id).all()


async def get_all_events_by_user_id_ongoing_in_specified_time(user_id: int, start: datetime,
                                                              end: datetime, db: Session):
    events = []
    for event in await get_all_events_of_user_by_user_id(user_id=user_id, db=db):
        while event is not None and event.event_date_start <= end:
            if event.event_date_end >= start:
                events += [event]
            event = event.next_event()
    return events


async def create_required_event_participants(db_event, db):
    for participant in db_event.specify_participants:
        db.add(models.DBEventParticipants(event_id=db_event.event_id, user_id=participant,
                                          participant_status="accepted" if participant == db_event.created_by
                                          else "pending",
                                          participant_role="host" if participant == db_event.created_by else "member",
                                          response_time=datetime.now()))  # TODO: zgadnij kiedy odpowie


async def create_event_categories(event_id: int, event: models.EventRequest, db: Session):
    for category_id in event.categories:
        db.add(models.DBEventCategory(event_id=event_id, category_id=category_id))


async def create_event_with_required_associations(event: models.EventRequest, db: Session):
    db_event = models.DBEvent.create(event)
    db.add(db_event)
    db.commit()
    await create_required_event_participants(db_event=db_event, db=db)
    await create_event_categories(event_id=db_event.event_id, event=event, db=db)
    db.commit()


async def create_event_participant(event_participants: str, db: Session):
    # TODO: consider is it useless and potentially remove (depends on future)
    db_event_participants = models.DBEventParticipants.create(event_participants)
    db.add(db_event_participants)
    db.commit()


async def create_category(category: models.CategoryRequest, db: Session):
    db_category = models.DBCategory.create(category)
    db.add(db_category)
    db.commit()


async def update_event(event_id: int, changed_data: models.EventRequest, db: Session):
    event = db.get(models.DBEvent, event_id)
    new_data = changed_data.dict(exclude_unset=True)
    for field, value in new_data.items():
        if field == "categories":
            await delete_all_event_categories(event_id=event_id, db=db)
            await create_event_categories(event_id=event_id, event=changed_data, db=db)
        else:
            if field == "privacy" and not event.privacy == value:
                await delete_all_event_participants(event_id=event_id, db=db)
                setattr(event, field, value)
                db.commit()
                await create_required_event_participants(db_event=event, db=db)
            else:
                setattr(event, field, value)
    db.commit()


async def update_category(category_id: int, changed_data: models.CategoryRequest, db: Session):
    category = db.get(models.DBCategory, category_id)
    new_data = changed_data.dict(exclude_unset=True)
    for field, value in new_data.items():
        setattr(category, field, value)
    db.commit()


async def delete_event_and_associated_objects(user_id: int, event_id: int, db: Session):
    event = db.get(models.DBEvent, event_id)
    if event.created_by == user_id:
        await delete_all_event_categories(event_id=event_id, db=db)
        await delete_all_event_participants(event_id=event_id, db=db)
        db.delete(event)
        db.commit()
    else:
        await accept_or_reject_participate_in_event(user_id=user_id, event_id=event_id, is_accepted=False, db=db)


async def accept_or_reject_participate_in_event(user_id: int, event_id: int, is_accepted: bool, db: Session):
    db_event_participant = db.query(models.DBEventParticipants).filter(
        models.DBEventParticipants.event_id == event_id and models.DBEventParticipants.user_id == user_id).first()
    if is_accepted:
        db_event_participant.participant_status = "accepted"
        db_event_participant.response_time = datetime.now()
    else:
        db.delete(db_event_participant)
    db.commit()



async def delete_all_event_participants(event_id: int, db: Session):
    db_event_participants = db.query(models.DBEventParticipants).filter(
        models.DBEventParticipants.event_id == event_id).all()
    for db_event_participant in db_event_participants:
        db.delete(db_event_participant)
    db.commit()


async def delete_all_event_categories(event_id: int, db: Session):
    db_event_categories = db.query(models.DBEventCategory).filter(
        models.DBEventCategory.event_id == event_id).all()
    for db_event_category in db_event_categories:
        db.delete(db_event_category)
    db.commit()


async def delete_category(category_id: int, db: Session):
    # TODO: Probably to remove
    category = db.get(models.DBCategory, category_id)
    db.delete(category)
    db.commit()


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
        friendship.action_time = datetime.now()

        db.commit()
        db.refresh(friendship)

        reversed_friendship = await get_friend_request(db, sender_id=recipient_id, recipient_id=sender_id)
        if reversed_friendship is None:
            # create entry for recipient -> sender
            await create_friend_request(db, sender_id=recipient_id, recipient_id=sender_id, friendship_status=action)
        else:
            reversed_friendship.friendship_status = action
            reversed_friendship.action_time = datetime.now()

            db.commit()
            db.refresh(reversed_friendship)

        return friendship
    return {"error": "Friend request not found"}