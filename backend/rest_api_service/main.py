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
       

@app.post("/friend-request/{recipient_id}", tags=['Friend'])
async def send_friend_request(recipient_id: int, db: Session = Depends(get_db)):
    sender_id = 1  
    friendship = DBUserFriendship(user1_id=sender_id, user2_id=recipient_id, friendship_status=friendship_status.pending)
    db.add(friendship)
    db.commit()
    return {"message": "Friend request sent successfully"}

@app.put("/friend-request/{request_id}/accept", tags=['Friend'])
async def accept_friend_request(request_id: int, db: Session = Depends(get_db)):
    friendship = db.query(DBUserFriendship).filter(DBUserFriendship.friendship_id == request_id).first()
    if friendship:
        if friendship.friendship_status == friendship_status.pending:
            friendship.friendship_status = friendship_status.accepted
            db.commit()
            return {"message": "Friend request accepted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Friend request has already been accepted")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend request not found")