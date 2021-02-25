from domains.user.repositories.user_role_repository import UserRoleRepository
from domains.user.schemas.user_schema import UserRole
from domains.user.repositories.user_repository import UserRepository
from domains.user.schemas.user_schema import UserCreate, UserDelete
from domains.user.models.user import User
from fastapi import HTTPException
from sqlalchemy.orm import Session


class UserFacade:
    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db=db)
        self.user_role_repository = UserRoleRepository(db=db)

    def create_user(self, username: str, password: str, user_role: UserRole) -> User:
        if self.user_repository.does_user_exist(username=username):
            raise HTTPException(status_code=400, detail="유저 이름이 중복됩니다.")

        selected_user_role = self.user_role_repository.get_user_role_by_name(user_role.value)
        if not selected_user_role:
            raise HTTPException(status_code=400, detail="유저 권한을 찾을 수 없습니다.")

        return self.user_repository.create_user(
            user=UserCreate(username=username, password=password, role_id=selected_user_role.id)
        )

    def delete_user(self, username: str) -> None:
        if not self.user_repository.does_user_exist(username=username):
            raise HTTPException(status_code=400, detail="유저를 찾을 수 없습니다")
        return self.user_repository.delete_user(user=UserDelete(username=username))