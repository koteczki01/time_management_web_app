import bcrypt
from fastapi import FastAPI, HTTPException, status, Depends, Response
import crud
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import *
import datetime
import pytz
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
utc = pytz.UTC


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
        time_now = utc.localize(datetime.now())

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
