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
import schemas


utc = pytz.UTC
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
async def register(user: UserRegisterSchema, response: Response, db: Session = Depends(get_db)):
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


@app.post("/friends/send", tags=['Friends'], status_code=status.HTTP_201_CREATED, response_model=schemas.Friendship|dict)
async def send_friend_request(sender_id: int, recipient_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        if sender_id == recipient_id:
            raise HTTPException(status_code=409, detail='Cannot send request to self')

        frienship = await crud.get_friend_request(db, sender_id, recipient_id)

        if frienship is None:
            friendship = await crud.create_friend_request(db, sender_id, recipient_id)

            if isinstance(friendship, dict) and friendship.get('error', None) is not None:
                raise HTTPException(status_code=404, detail=friendship['error'])

            return friendship

        raise HTTPException(status_code=409, detail='Friend request already sent')

    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")


@app.put("/friends/accept", tags=['Friends'], status_code=status.HTTP_200_OK, response_model=schemas.Friendship|dict)
async def accept_friend_request(sender_id: int, recipient_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        friendship_res = await crud.alter_friend_request(db, sender_id, recipient_id, "accepted")

        if isinstance(friendship_res, dict) and friendship_res.get('error', None) is not None:
            raise HTTPException(status_code=409, detail=friendship_res['error'])

        return friendship_res

    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.put("/friends/reject", tags=['Friends'], status_code=status.HTTP_200_OK, response_model=schemas.Friendship|dict)
async def reject_friend_request(sender_id: int, recipient_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        friendship_res = await crud.alter_friend_request(db, sender_id, recipient_id, "rejected")

        if isinstance(friendship_res, dict) and friendship_res.get('error', None) is not None:
            raise HTTPException(status_code=409, detail=friendship_res['error'])

        return friendship_res

    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}
