import bcrypt
from fastapi import FastAPI, HTTPException, status, Depends, Response
import crud
from database import SessionLocal
from sqlalchemy.orm import Session
from datetime import date
from schemas import *
from schemas import UserLoginSchema, UserRegisterSchema
import datetime
import pytz

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




@app.get("/users/get_user_by_id/{id}", tags = ['User'], status_code=status.HTTP_200_OK)
async def get__user_by_id(id : int, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_id(db, id)
        return user

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}

@app.get("/users/get_user_by_username/{username}", tags = ['User'], status_code=status.HTTP_200_OK)
async def get__user_by_username(username : str, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_username(db, username)
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
            if events_created:
                return events_created
            return {"message": "Events not found belonging to this user"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}
    

@app.get("/users/get_all_active_users", tags=['User'], status_code=status.HTTP_200_OK)
async def get_all_active_users( response: Response, db: Session = Depends(get_db)):
    try:
        active_users = await crud.get_all_active_users(db)     
        return active_users   
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}

@app.get("/users/get_all_friends_of_user_by_user_id/{user_id}", tags=['User'], status_code=status.HTTP_200_OK)
async def get_all_friends_of_user_by_user_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_id(db, user_id)
        if user:
            user_friends = await crud.get_all_friends_of_user_by_user_id(db, user_id)
            if user_friends:
                return user_friends
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User user has no friends :("}
        return {"message": "User not found"}
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


@app.put("/users/{user_id}/update_birthday", tags=['User'], status_code=status.HTTP_200_OK)
async def update_user_birthday(user_id: int, new_birthday: date, response: Response, db: Session = Depends(get_db)):
    try:
        updated_user = await crud.update_user_birthday(db, user_id, new_birthday)
        if updated_user:
            return updated_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


@app.put("/users/{user_id}/change_password", tags=['User'], status_code=status.HTTP_200_OK)
async def change_user_password(user_id: int, new_password_hash: str, response: Response, db: Session = Depends(get_db)):
    try:
        updated_user = await crud.change_user_password(db, user_id, new_password_hash)
        if updated_user:
            return updated_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}
    
@app.put("/users/{user_id}/change_email", tags=['User'], status_code=status.HTTP_200_OK)
async def change_user_email(user_id: int, new_email: str, response: Response, db: Session = Depends(get_db)):
    try:
        updated_user = await crud.change_user_email(db, user_id, new_email)
        if updated_user:
            return updated_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}
    
@app.put("/users/{user_id}/change_username", tags=['User'], status_code=status.HTTP_200_OK)
async def change_user_username(user_id: int, new_username: str, response: Response, db: Session = Depends(get_db)):
    try:
        updated_user = await crud.change_user_username(db, user_id, new_username)
        if updated_user:
            return updated_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


@app.put("/users/{user_id}/update_last_login", tags=['User'], status_code=status.HTTP_200_OK)
async def update_user_last_login(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        updated_user = await crud.update_user_last_login(db, user_id)
        if updated_user:
            return updated_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}
        

@app.get("/category/get_all_categories", tags=['Category'], status_code=status.HTTP_200_OK)
async def get_all_categories(response: Response, db: Session = Depends(get_db)):

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
