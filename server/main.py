from fastapi import Depends
from models.user import UserCreate, UserDelete, UserSchema, UserFacade, Base
from database import SessionLocal, engine
from fastapi import FastAPI
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/register/", response_model=UserSchema)
async def register(next_user: UserCreate, db=Depends(get_db)):
    user_facade = UserFacade(db=db)
    return user_facade.create_user(
        username=next_user.username, password=next_user.password
    )


@app.post("/users/remove")
async def remove(delete_user: UserDelete, db=Depends(get_db)):
    user_facade = UserFacade(db=db)
    user_facade.delete_user(username=delete_user.username)
    return {
        "message": f"[{delete_user.username}] 유저가 삭제되었습니다"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)