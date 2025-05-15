from sqlalchemy import Column, Integer, String
from ..database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    endpoint = Column(String, nullable=False)
    description = Column(String, nullable=True)
