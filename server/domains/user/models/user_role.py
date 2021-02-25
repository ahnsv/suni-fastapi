from database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String


class UserRole(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)

