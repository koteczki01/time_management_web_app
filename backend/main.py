from fastapi import FastAPI, status


app = FastAPI()


@app.get("/hello-world", tags=['Test'], status_code=status.HTTP_200_OK)
async def check_if_session_exists():
    try:

        return {"message": "Hello World"}

    except Exception as e:
        return {"message": f"An error occured: {e}"}
