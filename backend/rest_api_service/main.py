import datetime
import bcrypt
from fastapi import FastAPI, HTTPException, status, Depends, Response
import crud
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import *
from schemas import UserLoginSchema, UserRegisterSchema


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
    

@app.post("/login", tags=['User'], status_code=status.HTTP_200_OK)
async def login(login_schema: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    try: 
        user = await crud.get_user_by_username(db, login_schema.username.lower())
        if user != None and bcrypt.checkpw(login_schema.password_hash.encode('utf-8'), user.password_hash.encode('utf-8')):
            await crud.update_user_last_login(db, user.user_id)
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}
    

@app.post("/register", tags=['User'], status_code=status.HTTP_201_CREATED)
async def register(user : UserRegisterSchema, response: Response, db: Session = Depends(get_db)):
    try:
        existing_user = await crud.get_user_by_username(db, user.username.lower())
        
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        if user.birthday > datetime.datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Birthday cannot be in the future")

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(rounds=8))

        new_user = await crud.create_user(db, username=user.username.lower(), email=user.email, password_hash = hashed_password.decode('utf-8'), birthday=user.birthday)

        return new_user
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}