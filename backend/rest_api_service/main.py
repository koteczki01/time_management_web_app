import datetime
import bcrypt
from fastapi import FastAPI, HTTPException, status, Depends, Response
import crud
from database import SessionLocal
from sqlalchemy.orm import Session


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
    

@app.get("/login/{username}", tags=['User'], status_code=status.HTTP_200_OK)
async def login(username: str, password: str, response: Response, db: Session = Depends(get_db)):
    try: 
        user = await crud.get_user_by_username(db, username)

        if(bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))):
            await crud.update_user_last_login(db, user.user_id)
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occured: {e}"}
    

@app.post("/register", tags=['User'], status_code=status.HTTP_201_CREATED)
async def register(username: str, password: str, email : str, birthday : datetime.datetime, response: Response, db: Session = Depends(get_db)):
    try:
        # Check if the username already exists
        existing_user = await crud.get_user_by_username(db, username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=8))

        # Create a new user
        new_user = await crud.create_user(db, username=username, email=email, password_hash = hashed_password.decode('utf-8'), birthday=birthday)

        return new_user
    except Exception as e:
        response.status_code = 500
        return {"message": f"An error occurred: {e}"}