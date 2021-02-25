from domains.user.models.user import User
from domains.user.schemas.user_schema import UserCreate, UserDelete
from sqlalchemy.orm.session import Session


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