from fastapi import FastAPI, status, Depends, Response, HTTPException, Security
import crud
from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt
from datetime import timedelta
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base as db_base
from schemas import UserLoginSchema, UserRegisterSchema
import bcrypt
import pytz
import datetime

utc = pytz.UTC
app = FastAPI()

# Konfiguracja połączenia z bazą danych
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/Database"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = db_base()

# Model danych użytkownika
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# Konfiguracja uwierzytelniania
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Model Pydantic dla danych wejściowych
class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    birthday: datetime.date

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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

username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

MAX_LOGIN_ATTEMPTS = 3  # Maksymalna liczba prób logowania przed zablokowaniem konta
LOCKOUT_DURATION_MINUTES = 5  # Czas blokady konta w minutach po przekroczeniu maksymalnej liczby prób
@app.post("/login", tags=['User'], status_code=status.HTTP_200_OK, response_model=UserLoginResponse | ErrorOccured)
async def login(login_schema: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    try:
        user = await crud.get_user_by_username(db, login_schema.username.lower())
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exists")

        # Sprawdza czy konto jest zablokowane
        if await is_account_locked(db, user.id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account temporarily blocked")

        if bcrypt.checkpw(login_schema.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            await crud.update_user_last_login(db, user.id)
            await reset_login_attempts(db, user.id)  # Zresetuj liczbę prób logowania
            return user
        else:
            await update_login_attempts(db, user.id)  # Zaktualizuj liczbę prób logowania
            if await is_account_locked(db, user.id):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account temporarily blocked")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": f"An error occurred: {e}"}


async def is_account_locked(db: Session, user_id: int) -> bool:
    user = await crud.get_user(db, user_id)
    if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
        if user.last_login_attempt and user.last_login_attempt + timedelta(
                minutes=LOCKOUT_DURATION_MINUTES) > datetime.now():
            return True
    return False


@app.post("/register", tags=['User'], status_code=status.HTTP_201_CREATED,
          response_model=dict | ErrorOccured)
async def register(user: UserRegisterSchema, response: Response, db: Session = Depends(get_db)):
    try:
        existing_user = await crud.get_user_by_username(db, user.username.lower())

        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        # walidacja adresu e-mail
        if not EmailValidator.validate_email(user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address")

        # Sprawdza czy data urodzenia jest mozliwa
        if user.birthday and user.birthday > datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Birthday cannot be in the future")

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(rounds=8))

        new_user = await crud.create_user(db, username=user.username.lower(), email=user.email,
                                          password_hash=hashed_password.decode('utf-8'), birthday=user.birthday)

        if new_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Something went wrong while creating user")

        # Zwraca podstawowe informacje o użytkowniku jako słownik
        return {"id": new_user.id, "username": new_user.username}
    except HTTPException as e:
        response.status_code = e.status_code
        return {"message": e.detail}
    except Exception as e:
        response.status_code = 500
    return {"message": f"An error occured: {e}"}



# Endpoint do generowania tokena JWT po poprawnym uwierzytelnieniu
@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        # Generowanie tokena JWT
        token_data = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.utcnow() + access_token_expires
        }
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# Endpoint wymagający autoryzacji
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "You are authorized!"}
