from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from database import Base
from sqlalchemy.sql.sqltypes import Boolean, Integer, String
from sqlalchemy import Column


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(
        String,
        unique=True,
    )
    password = Column(String)
    is_activate = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    roles = relationship("UserRole")

