from fastapi import FastAPI, status, Depends, Response
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


@app.post("/friend-request/{recipient_id}", tags=['Friend'], status_code=status.HTTP_201_CREATED)
async def send_friend_request(recipient_id: int, db: Session = Depends(get_db)):
    try:
        
        friendship = crud.create_friend_request(db, sender_id, recipient_id)
        return {"message": "Pomyœlnie zaproszono u¿ytkownika do grona znajomych"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")


@app.put("/friend-request/{sender_id}/accept", tags=['Friend'], status_code=status.HTTP_200_OK)
async def accept_friend_request(sender_id: int, db: Session = Depends(get_db)):
    try:
        
        friendship = crud.get_friend_request(db, sender_id) 
        if friendship:
            if friendship.friendship_status == friendship_status.pending:
                friendship.friendship_status = friendship_status.accepted
                db.commit()
                return {"message": "Friend request accepted successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Friend request has already been accepted")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend request not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")

