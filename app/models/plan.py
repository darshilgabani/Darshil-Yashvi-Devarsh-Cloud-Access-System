from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    api_permissions = Column(JSON, nullable=False)
    usage_limits = Column(JSON, nullable=False)

    subscriptions = relationship("Subscription", back_populates="plan")
