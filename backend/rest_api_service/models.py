from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime, timezone


# Define your ENUM types
privacy_level = ENUM('public', 'private', name="privacy_level", create_type=False)
status = ENUM('pending', 'accepted', name="status", create_type=False)
recurrence_rule = ENUM('daily', 'weekly', 'monthly', 'yearly', name="recurrence_rule", create_type=False)
event_role = ENUM('host', 'member', name="event_role", create_type=False)


association_user_friendships = Table('association_user_friendships', Base.metadata,
    Column('user_id', Integer, ForeignKey('db_user.user_id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('db_user.user_id'), primary_key=True)
)

class DBCategory(Base):
    __tablename__ = 'db_category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(45), unique=True)
    category_description = Column(String(255))

    events = relationship("DBEvent", secondary="db_event_category", back_populates="categories")


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


class DBEvent(Base):
    __tablename__ = 'db_event'

    event_id = Column(Integer, primary_key=True)
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


class DBEventCategory(Base):
    __tablename__ = 'db_event_category'

    event_id = Column(Integer, ForeignKey('db_event.event_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('db_category.category_id'), primary_key=True)


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
