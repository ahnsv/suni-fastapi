from database import Base
from fastapi import HTTPException
from sqlalchemy.sql.sqltypes import Boolean, Integer, String
from sqlalchemy import Column
from sqlalchemy.orm import Session
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(
        String,
        unique=True,
    )
    password = Column(String)
    is_activate = Column(Boolean, default=True)


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserDelete(UserBase):
    pass


class UserSchema(UserBase):
    id: int
    is_activate: bool = True

    class Config:
        orm_mode = True


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.model = User
        self.db = db

    def get_user_by_username(self, username: str) -> User:
        """유저 네임으로 유저를 검색합니다.

        Args:
            username (str): 유저 이름

        Returns:
            User: 유저 엔티티
        """
        return self.db.query(User).filter(User.username == username).first()

    def does_user_exist(self, username: str) -> bool:
        """유저가 데이터베이스에 존재하는 지 체크합니다. 존재하면 True, 없으면 False를 리턴합니다

        Args:
            username (str): 유저 네임

        Returns:
            bool: True/False
        """
        return self.get_user_by_username(username=username) is not None

    def create_user(self, user: UserCreate) -> User:
        """User를 생성합니다.

        Args:
            user (UserCreate): User Creation DTO
        """
        user_entry = User(**user.dict())
        self.db.add(user_entry)
        self.db.commit()
        self.db.refresh(user_entry)
        return user_entry

    def delete_user(self, user: UserDelete) -> None:
        delete_user = self.get_user_by_username(username=user.username)
        self.db.delete(delete_user)
        self.db.commit()


class UserFacade:
    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db=db)

    def create_user(self, username: str, password: str) -> User:
        if self.user_repository.does_user_exist(username=username):
            raise HTTPException(status_code=400, detail="유저 이름이 중복됩니다.")
        return self.user_repository.create_user(
            user=UserCreate(username=username, password=password)
        )

    def delete_user(self, username: str) -> None:
        if not self.user_repository.does_user_exist(username=username):
            raise HTTPException(status_code=400, detail="유저를 찾을 수 없습니다")
        return self.user_repository.delete_user(user=UserDelete(username=username))
