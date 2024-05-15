import bcrypt
from fastapi import FastAPI, HTTPException, status, Depends, Response
import crud
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import *
from schemas import UserLoginSchema, UserRegisterSchema
import datetime
import pytz

import models

utc=pytz.UTC
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login", tags=['User'], status_code=status.HTTP_200_OK, response_model=UserLoginResponse|ErrorOccured)
async def login(login_schema: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    try: 
        user = await crud.get_user_by_username(db, login_schema.username.lower())
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exists")
        if bcrypt.checkpw(login_schema.password_hash.encode('utf-8'), user.password_hash.encode('utf-8')):
            await crud.update_user_last_login(db, user.user_id)
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


@app.post("/register", tags=['User'], status_code=status.HTTP_201_CREATED, response_model=UserRegisterResponse|ErrorOccured)
async def register(user : UserRegisterSchema, response: Response, db: Session = Depends(get_db)):
    try:
        existing_user = await crud.get_user_by_username(db, user.username.lower())
        
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        # user_birthday = utc.localize(user.birthday)
        time_now = utc.localize(datetime.datetime.now())

        if user.birthday > time_now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Birthday cannot be in the future")

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(rounds=8))

        new_user = await crud.create_user(db, username=user.username.lower(), email=user.email, password_hash = hashed_password.decode('utf-8'), birthday=user.birthday)

        if new_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong while creating user")

        return new_user
    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event/get_all_participants", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_participants(response: Response, db: Session = Depends(get_db)):
    try:
        participants = await crud.get_all_participants(db)

        return participants

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event/{event_id}", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_event_by_id(event_id, response: Response, db: Session = Depends(get_db)):
    try:
        event = await crud.get_event_by_id(event_id=event_id, db=db)
        return event
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/user/{user_id}/events", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_of_user_by_user_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        events = await crud.get_all_events_of_user_by_user_id(user_id=user_id, db=db)
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event/crated_by/{user_id}", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_by_creator_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        events = await crud.get_all_events_by_creator_id(user_id=user_id, db=db)
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event/{event_id}/participants", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_event_participants(event_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        events = await crud.get_all_event_participants(event_id=event_id, db=db)
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/user/{user_id}/events/range_of_time/", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_by_user_id_ongoing_in_specified_time(user_id: int, start: datetime.datetime,
                                                              end: datetime.datetime, response: Response,
                                                              db: Session = Depends(get_db)):
    try:
        events = await crud.get_all_events_by_user_id_ongoing_in_specified_time(user_id=user_id, start=start, end=end,
                                                                                db=db)
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.post("/event/create/", tags=['Event'], status_code=status.HTTP_201_CREATED)
async def create_event_with_required_associations(event: models.EventRequest, response: Response,
                                                  db: Session = Depends(get_db)):
    try:
        await crud.create_event_with_required_associations(event=event, db=db)
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.post("/event/participants/create/{participant}", tags=['Event'], status_code=status.HTTP_201_CREATED)
# TODO: This probably is useless. consider this theory
async def create_event_participant(participant: str, response: Response, db: Session = Depends(get_db)):
    try:
        await crud.create_event_participant(event_participants=participant, db=db)
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.post("/category/create/", tags=['Category'], status_code=status.HTTP_201_CREATED)
async def create_category(category: models.CategoryRequest, response: Response, db: Session = Depends(get_db)):
    try:
        await crud.create_category(category=category, db=db)
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.put("/event/{event_id}/update/", tags=['Event'], status_code=status.HTTP_200_OK)
async def update_event(event_id: int, changed_data: models.EventRequest, response: Response,
                       db: Session = Depends(get_db)):
    try:
        await crud.update_event(event_id=event_id, changed_data=changed_data, db=db)
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.put("/category/{category_id}/update/", tags=['Category'], status_code=status.HTTP_200_OK)
async def update_category(category_id: int, changed_data: models.CategoryRequest, response: Response,
                          db: Session = Depends(get_db)):
    try:
        await crud.update_category(category_id=category_id, changed_data=changed_data, db=db)
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.delete("/event/{event_id}/delete", tags=['Event'], status_code=status.HTTP_200_OK)
async def delete_event(event_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        await crud.delete_event(event_id=event_id, db=db)
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.delete("/category/{category_id}/delete", tags=['Category'], status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        await crud.delete_category(category_id=category_id, db=db)
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}
