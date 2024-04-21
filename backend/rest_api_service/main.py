from fastapi import FastAPI, status, Depends, Response
import crud
from database import SessionLocal
from sqlalchemy.orm import Session
from datetime import date


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





@app.get("/users/get_user_by_id/{id}", tags = ['User'], status_code=status.HTTP_200_OK)
async def get__user_by_id(id : int, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_id(db, id)
        print(id)
        return user

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}

@app.get("/users/get_user_by_username/{username}", tags = ['User'], status_code=status.HTTP_200_OK)
async def get__user_by_username(username : str, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_username(db, username)
        print(username)
        return user

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}
    
@app.get("/users/get_all_events_by_user_id/{user_id}", tags=['User'], status_code=status.HTTP_200_OK)
async def get_all_events_by_user_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_id(db, user_id)
        if user:
            events_created = user.events_created
            return events_created
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}

@app.get("/users/get_all_friends_by_user_id/{user_id}", tags=['User'], status_code=status.HTTP_200_OK)
async def get_all_friends_by_user_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        user_friends = await crud.get_all_friends_by_user_id(db, user_id)
        if user_friends:
            return user_friends
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User not found or user has no friends"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}

@app.post("/users/create_user", tags=['User'], status_code=status.HTTP_201_CREATED)
async def create_user(response: Response, username: str, email: str, password_hash: str, birthday: date, is_active: bool = True, db: Session = Depends(get_db)):
    try:
        new_user = await crud.create_user(db, username, email, password_hash, birthday, is_active)
        return new_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}

@app.delete("/users/delete_user/{user_id}", tags=['User'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        success = await crud.delete_user(db, user_id)
        if success:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}



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
