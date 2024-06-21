import bcrypt
import crud
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import *
import pytz
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta, UTC, date
from dotenv import load_dotenv
import os
from models import *
from fastapi import FastAPI, HTTPException, status, Depends, Response
from typing import Union
from fastapi.middleware.cors import CORSMiddleware


# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
utc = pytz.UTC

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = await crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", tags=['Jwt'] , response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await crud.get_user_by_username(db, form_data.username.lower())
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", tags=['Jwt'], response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    return current_user


@app.post("/login", tags=['User'], status_code=status.HTTP_200_OK, response_model=UserLoginResponse | ErrorOccured)
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


@app.get("/users/get_user_by_id", tags=['User'], status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_id(db, id)
        return user

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/users/get_user_by_username", tags=['User'], status_code=status.HTTP_200_OK)
async def get_user_by_username(username: str, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_username(db, username)
        return user

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}


@app.get("/users/get_all_active_users", tags=['User'], status_code=status.HTTP_200_OK)
async def get_all_active_users(response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        active_users = await crud.get_all_active_users(db)
        return active_users
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


@app.get("/users/get_all_user_friends", tags=['User'], status_code=status.HTTP_200_OK)
async def get_all_user_friends(user_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_id(db, user_id)
        if user:
            user_friends = await crud.get_all_friends_of_user_by_user_id(db, user_id)
            if user_friends:
                return user_friends
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "You don't have any friends!"}
        return {"message": "User not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


@app.post("/users/create_user", tags=['User'], status_code=status.HTTP_201_CREATED)
async def create_user(response: Response, username: str, email: str, password_hash: str, birthday: date,
                      is_active: bool = True, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        new_user = await crud.create_user(db, username, email, password_hash, birthday, is_active)
        return new_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


@app.put("/users/update_birthday", tags=['User'], status_code=status.HTTP_200_OK)
async def update_user_birthday(user_id: int, new_birthday: date, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        updated_user = await crud.update_user_birthday(db, user_id, new_birthday)
        if updated_user:
            return updated_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


# @app.put("/users/{user_id}/change_password", tags=['User'], status_code=status.HTTP_200_OK)
# async def change_user_password(user_id: int, new_password_hash: str, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
#     try:
#         updated_user = await crud.change_user_password(db, user_id, new_password_hash)
#         if updated_user:
#             return updated_user
#     except Exception as e:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {"message": f"An error occurred: {e}"}


@app.put("/users/change_email", tags=['User'], status_code=status.HTTP_200_OK)
async def change_user_email(user_id: int, new_email: str, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        updated_user = await crud.change_user_email(db, user_id, new_email)
        if updated_user:
            return updated_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


@app.put("/users/change_username", tags=['User'], status_code=status.HTTP_200_OK)
async def change_user_username(user_id: int, new_username: str, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        updated_user = await crud.change_user_username(db, user_id, new_username)
        if updated_user:
            return updated_user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


@app.put("/users/change_password", tags=['User'], status_code=status.HTTP_200_OK)
async def change_password(user_id: int, password: str, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=8))
        user = await crud.change_password(db, user_id, hashed_password.decode('utf-8'))
        return user
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}
    

@app.post("/register", tags=['User'], status_code=status.HTTP_201_CREATED,
          response_model=UserRegisterResponse | ErrorOccured)
async def register(user: UserRegisterSchema, response: Response, db: Session = Depends(get_db)):
    try:
        existing_user = await crud.get_user_by_username(db, user.username.lower())

        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        # user_birthday = utc.localize(user.birthday)
        time_now = utc.localize(datetime.now())

        if user.birthday > time_now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Birthday cannot be in the future")

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(rounds=8))

        new_user = await crud.create_user(db, username=user.username.lower(), email=user.email,
                                          password_hash=hashed_password.decode('utf-8'), birthday=user.birthday)

        if new_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Something went wrong while creating user")

        return new_user
    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event/get_all_participants", tags=['EventParticipants'], status_code=status.HTTP_200_OK)
async def get_all_participants(response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        participants = await crud.get_all_participants(db)

        return participants

    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_event_by_id(event_id, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        event = await crud.get_event_by_id(event_id=event_id, db=db)
        return event
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/events/get_user_events", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_of_user_by_user_id(user_id: int, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        events = await crud.get_all_events_of_user_by_user_id(user_id=user_id, db=db)
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event/crated_by", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_by_creator_id(user_id: int, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        events = await crud.get_all_events_by_creator_id(user_id=user_id, db=db)
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/event/participants", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_event_participants(event_id: int, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        events = await crud.get_all_event_participants(event_id=event_id, db=db)
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.get("/events/range_of_time", tags=['Event'], status_code=status.HTTP_200_OK)
async def get_all_events_by_user_id_ongoing_in_specified_time(user_id: int, start: datetime,
                                                              end: datetime, response: Response,
                                                              db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        events = await crud.get_all_events_by_user_id_ongoing_in_specified_time(user_id=user_id, start=start, end=end,
                                                                                db=db)
        return events
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.post("/event/create", tags=['Event'], status_code=status.HTTP_201_CREATED)
async def create_event_with_required_associations(event: EventRequest, response: Response,
                                                  db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        await crud.create_event_with_required_associations(event=event, db=db)
        return {"message": "created successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.post("/category/create", tags=['Category'], status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryRequest, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        await crud.create_category(category=category, db=db)
        return {"message": "created successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.put("/event/update", tags=['Event'], status_code=status.HTTP_200_OK)
async def update_event(event_id: int, changed_data: EventRequest, response: Response,
                       db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        await crud.update_event(event_id=event_id, changed_data=changed_data, db=db)
        return {"message": "updated successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.put("/category/update", tags=['Category'], status_code=status.HTTP_200_OK)
async def update_category(category_id: int, changed_data: CategoryRequest, response: Response,
                          db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        await crud.update_category(category_id=category_id, changed_data=changed_data, db=db)
        return {"message": "updated successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.put("/event/participants/accept_or_reject", tags=['EventParticipants'], status_code=status.HTTP_200_OK)
async def accept_or_reject_participate_in_event(user_id: int, event_id: int, is_accepted: bool, response: Response,
                                                db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        res = await crud.accept_or_reject_participate_in_event(user_id=user_id, event_id=event_id,
                                                                is_accepted=is_accepted, db=db)
        return res
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.delete("/event/delete", tags=['Event'], status_code=status.HTTP_200_OK)
async def delete_event_and_associated_objects(user_id: int, event_id: int, response: Response,
                                              db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        await crud.delete_event_and_associated_objects(user_id=user_id, event_id=event_id, db=db)
        return {"message": "deleted successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.delete("/category/delete", tags=['Category'], status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    try:
        await crud.delete_category(category_id=category_id, db=db)
        return {"message": "deleted successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}


@app.put("/friends/reject", tags=['Friends'], status_code=status.HTTP_200_OK, response_model=Friendship|dict)
async def reject_friend_request(sender_id: int, recipient_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        friendship_res = await crud.alter_friend_request(db, sender_id, recipient_id, "rejected")

        if isinstance(friendship_res, dict) and friendship_res.get('error', None) is not None:
            raise HTTPException(status_code=409, detail=friendship_res['error'])

        return friendship_res

    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}


@app.post("/friends/send", tags=['Friends'], status_code=status.HTTP_201_CREATED, response_model=Friendship|dict)
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


@app.put("/friends/accept", tags=['Friends'], status_code=status.HTTP_200_OK, response_model=Friendship|dict)
async def accept_friend_request(sender_id: int, recipient_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        friendship_res = await crud.alter_friend_request(db, sender_id, recipient_id, "accepted")

        if isinstance(friendship_res, dict) and friendship_res.get('error', None) is not None:
            raise HTTPException(status_code=409, detail=friendship_res['error'])

        return friendship_res

    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}


@app.put("/friends/cancel", tags=['Friends'], status_code=status.HTTP_200_OK, response_model=Friendship|dict)
async def reject_friend_request(sender_id: int, recipient_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        friendship_res = await crud.alter_friend_request(db, sender_id, recipient_id, "cancelled")

        if isinstance(friendship_res, dict) and friendship_res.get('error', None) is not None:
            raise HTTPException(status_code=409, detail=friendship_res['error'])

        return friendship_res

    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}
