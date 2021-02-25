from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from applications.facade.user_facade import UserFacade
from database import Base, SessionLocal, engine
from domains.user.models.user_role import UserRole
from domains.user.schemas.user_schema import UserCreateRequest, UserDelete
from domains.user.schemas.user_schema import UserSchema

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup(db: Session = SessionLocal()):
    """Initial Data Loading"""
    if not db.query(UserRole).first():
        db.add(UserRole(name="admin"))
        db.add(UserRole(name="parent"))
        db.add(UserRole(name="student"))
        db.add(UserRole(name="teacher"))
        db.commit()


@app.on_event("shutdown")
async def shutdown(db: Session = SessionLocal()):
    """Initial Data Loading"""
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        print("Clear table {table}", table)
        db.execute(table.delete())
    db.commit()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/register/", response_model=UserSchema)
async def register(next_user: UserCreateRequest, db=Depends(get_db)):
    user_facade = UserFacade(db=db)
    return user_facade.create_user(
        username=next_user.username,
        password=next_user.password,
        user_role=next_user.role,
    )


@app.post("/users/remove")
async def remove(delete_user: UserDelete, db=Depends(get_db)):
    user_facade = UserFacade(db=db)
    user_facade.delete_user(username=delete_user.username)
    return {"message": f"[{delete_user.username}] 유저가 삭제되었습니다"}
