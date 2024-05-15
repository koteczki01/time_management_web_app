from fastapi import FastAPI, status, Depends, Response
import crud
from database import SessionLocal
from sqlalchemy.orm import Session
import datetime

import models

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
        return {"message": f"An error occurred: {e}"}


@app.get("/category/get_all_categories", tags=['Category'], status_code=status.HTTP_200_OK)
async def get_all_categories(response: Response, db: Session = Depends(get_db)):
    try:
        categories = await crud.get_all_categories(db)

        return categories

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event/get_all_events", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events(response: Response, db: Session = Depends(get_db)):
    try:
        events = await crud.get_all_events(db)

        return events

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
