from fastapi import FastAPI, status, Depends, Response
import crud
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import datetime

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/get_all_users", tags=['User'], status_code=status.HTTP_200_OK)
async def get_all_users(response: Response, db: Session = Depends(get_db)):
    try:
        users = await crud.get_all_users(db)

        return users

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/category/get_all_categories", tags=['Category'], status_code=status.HTTP_200_OK)
async def get_all_categories(response: Response, db: Session = Depends(get_db)):
    try:
        categories = await crud.get_all_categories(db)

        return categories

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/event/get_all_events", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events(response: Response, db: Session = Depends(get_db)):
    try:
        events = await crud.get_all_events(db)

        return events

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/event/get_all_participants", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_participants(response: Response, db: Session = Depends(get_db)):
    try:
        participants = await crud.get_all_participants(db)

        return participants

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/event/{event_id}", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_event_by_id(event_id, response: Response, db: Session = Depends(get_db)):
    try:
        return db.get(models.DBEvent, event_id)
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/user/{user_id}/events", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_of_user_by_user_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        return db.query(models.DBEvent).join(models.DBEventParticipants).filter(
            models.DBEventParticipants.user_id == user_id).all()
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/event/crated_by/{user_id}", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_by_creator_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        return db.query(models.DBEvent).filter(
            models.DBEvent.created_by == user_id).all()
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/event/{event_id}/participants", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_event_participants(event_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        return db.query(models.DBUser).join(models.DBEventParticipants).filter(
            models.DBEventParticipants.event_id == event_id).all()
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/user/{user_id}/events/range_of_time/{start, end}", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_by_user_id_ongoing_in_specified_time(user_id: int, start: datetime.datetime,
                                                              end: datetime.datetime, response: Response,
                                                              db: Session = Depends(get_db)):
    try:
        events = []
        for event in db.query(models.DBEvent).join(models.DBEventParticipants).filter(
                models.DBEventParticipants.user_id == user_id).all():
            while event is not None and event.event_date_start <= end and event.event_date_end >= start:
                events += [event]
                event = event.next_event()
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}
# 2024-10-10T10:10:10