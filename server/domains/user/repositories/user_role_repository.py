from sqlalchemy.orm.session import Session
from domains.user.models.user_role import UserRole


class UserRoleRepository:
    def __init__(self, db: Session) -> None:
        self.model = UserRole
        self.db = db

    def get_user_role_by_name(self, role_name: str) -> UserRole:
        return self.db.query(UserRole).filter(UserRole.name == role_name).first()
