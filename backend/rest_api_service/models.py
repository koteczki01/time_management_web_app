import json
from typing import Optional
from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, Date, Table, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime, timezone, timedelta

# Define your ENUM types
privacy_level = ENUM('public', 'private', name="privacy_level", create_type=False)
status = ENUM('pending', 'accepted', name="status", create_type=False)
recurrence_rule = ENUM('daily', 'weekly', 'monthly', 'yearly', name="recurrence_rule", create_type=False)
event_role = ENUM('host', 'member', name="event_role", create_type=False)

association_user_friendships = Table('association_user_friendships', Base.metadata,
                                     Column('user_id', Integer, ForeignKey('db_user.user_id'), primary_key=True),
                                     Column('friend_id', Integer, ForeignKey('db_user.user_id'), primary_key=True)
                                     )


class CategoryRequest(BaseModel):
    category_name: str | None = None
    category_description: str | None = None


class DBCategory(Base):
    __tablename__ = 'db_category'

    category_id = Column(Integer, Sequence('db_category_id_seq'), primary_key=True)
    category_name = Column(String(45), unique=True)
    category_description = Column(String(255))

    events = relationship("DBEvent", secondary="db_event_category", back_populates="categories")

    def __init__(self, category_id, category_name, category_description):
        self.category_id = category_id
        self.category_name = category_name
        self.category_description = category_description

    @staticmethod
    def create(category: CategoryRequest):
        return DBCategory(
            category_id=None,
            category_name=category.category_name,
            category_description=category.category_description)


class DBUser(Base):
    __tablename__ = 'db_user'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(45), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    last_login = Column(TIMESTAMP, nullable=False)
    update_date = Column(TIMESTAMP, nullable=False, onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, nullable=False)

    events_created = relationship("DBEvent", back_populates="creator")
    participated_events = relationship("DBEventParticipants", back_populates="user")

    friends = relationship(
        'DBUser',
        secondary=association_user_friendships,
        primaryjoin=user_id == association_user_friendships.c.user_id,
        secondaryjoin=user_id == association_user_friendships.c.friend_id,
        backref="friended_by"
    )


class EventRequest(BaseModel):
    created_by: int | None = None
    event_name: str | None = None
    event_description: str | None = None
    event_date_start: datetime | None = None
    event_date_end: datetime | None = None
    event_location: str | None = None
    privacy: str | None = None
    recurrence: str | None = None
    next_event_date: datetime | None = None
    categories: list | None = None


class DBEvent(Base):
    __tablename__ = 'db_event'

    event_id = Column(Integer, Sequence('db_event_id_seq'), primary_key=True)
    created_by = Column(Integer, ForeignKey('db_user.user_id'), nullable=False)
    event_name = Column(String(60), nullable=False)
    event_description = Column(String(255))
    event_date_start = Column(TIMESTAMP, nullable=False)
    event_date_end = Column(TIMESTAMP, nullable=False)
    event_location = Column(String(255))
    privacy = Column(privacy_level, nullable=False)
    recurrence = Column(recurrence_rule, nullable=False)
    next_event_date = Column(TIMESTAMP)

    creator = relationship("DBUser", back_populates="events_created")
    categories = relationship("DBCategory", secondary="db_event_category", back_populates="events")
    participants = relationship("DBEventParticipants", back_populates="event")

    @property
    def specify_participants(self):
        if self.privacy == "private":
            return [self.created_by]
        if self.privacy == "public":
            return [self.created_by]  # +friends# TODO: read it from db (pending) - I need to get friends :(

    def __init__(self, event_id, created_by, event_name, event_description, event_date_start, event_date_end,
                 event_location, privacy, recurrence, next_event_date):
        self.event_id = event_id
        self.created_by = created_by
        self.event_name = event_name
        self.event_description = event_description
        self.event_date_start = event_date_start
        self.event_date_end = event_date_end
        self.event_location = event_location
        self.privacy = privacy
        self.recurrence = recurrence
        self.next_event_date = next_event_date

    @staticmethod
    def create(event: EventRequest):
        return DBEvent(
            event_id=None,
            created_by=event.created_by,
            event_name=event.event_name,
            event_description=event.event_description,
            event_date_start=event.event_date_start,
            event_date_end=event.event_date_end,
            event_location=event.event_location,
            privacy=event.privacy,
            recurrence=event.recurrence,
            next_event_date=event.next_event_date
        )

    def copy(self):
        return DBEvent(
            self.event_id,
            self.created_by,
            self.event_name,
            self.event_description,
            self.event_date_start,
            self.event_date_end,
            self.event_location,
            self.privacy,
            self.recurrence,
            self.next_event_date,
        )

    def replace_date(self, date: datetime):
        if self.recurrence == "daily":
            return date + timedelta(days=1)
        if self.recurrence == "weekly":
            return date + timedelta(weeks=1)
        if self.recurrence == "monthly":
            if date.month == 12:
                return date.replace(month=1, year=date.year + 1)
            return date.replace(month=date.month + 1)
        if self.recurrence == "yearly":
            return date.replace(year=date.year + 1)

    def next_event(self):
        if recurrence_rule is None:
            # I know it impossible, but I don't know why xD
            return None
        next_instance = DBEvent.copy(self)
        next_instance.event_date_start = next_instance.replace_date(next_instance.event_date_start)
        next_instance.event_date_end = next_instance.replace_date(next_instance.event_date_end)
        next_instance.next_event_date = next_instance.replace_date(next_instance.next_event_date)
        return next_instance


class DBEventCategory(Base):
    __tablename__ = 'db_event_category'

    event_id = Column(Integer, ForeignKey('db_event.event_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('db_category.category_id'), primary_key=True)

    def __init__(self, event_id, category_id):
        self.event_id = event_id
        self.category_id = category_id


class DBUserFriendship(Base):
    __tablename__ = 'db_user_friendship'

    friendship_id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey('db_user.user_id'), nullable=False)
    user2_id = Column(Integer, ForeignKey('db_user.user_id'), nullable=False)
    friendship_status = Column(status, nullable=False)


class DBEventParticipants(Base):
    __tablename__ = 'db_event_participants'

    event_id = Column(Integer, ForeignKey('db_event.event_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('db_user.user_id'), primary_key=True)
    participant_status = Column(status, nullable=False)
    participant_role = Column(event_role, nullable=False)
    response_time = Column(TIMESTAMP, nullable=False)

    user = relationship("DBUser", back_populates="participated_events")
    event = relationship("DBEvent", back_populates="participants")

    def __init__(self, event_id, user_id, participant_status, participant_role, response_time):
        self.event_id = event_id
        self.user_id = user_id
        self.participant_status = participant_status
        self.participant_role = participant_role
        self.response_time = response_time

    @staticmethod
    def create(participant: str):
        participant = json.loads(participant)
        return DBEventParticipants(
            event_id=participant['event_id'],
            user_id=participant['user_id'],
            participant_status=participant['participant_status'],
            participant_role=participant['participant_role'],
            response_time=participant['response_time']
        )
