from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    api_name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="usage_logs")
