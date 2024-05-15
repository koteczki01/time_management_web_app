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


async def get_all_events_by_user_id_ongoing_in_specified_time(user_id: int, start: datetime.datetime,
                                                              end: datetime.datetime, db: Session):
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
                                          response_time=datetime.datetime.now()))  # TODO: zgadnij kiedy odpowie


async def create_event_with_required_associations(event: models.EventRequest, db: Session):
    db_event = models.DBEvent.create(event)
    db.add(db_event)
    db.commit()
    await create_required_event_participants(db_event=db_event, db=db)
    for category_id in event.categories:
        db.add(models.DBEventCategory(event_id=db_event.event_id, category_id=category_id))
    db.commit()


async def create_event_participant(event_participants: str, db: Session):
    # TODO: consider is it useless and potentially remove
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
        setattr(event, field, value)
    db.commit()


async def update_category(category_id: int, changed_data: models.CategoryRequest, db: Session):
    category = db.get(models.DBCategory, category_id)
    new_data = changed_data.dict(exclude_unset=True)
    for field, value in new_data.items():
        setattr(category, field, value)
    db.commit()


async def delete_event(event_id: int, db: Session):
    event = db.get(models.DBEvent, event_id)
    # TODO: delete all associations
    db.delete(event)
    db.commit()


async def delete_category(category_id: int, db: Session):
    category = db.get(models.DBCategory, category_id)
    db.delete(category)
    db.commit()
