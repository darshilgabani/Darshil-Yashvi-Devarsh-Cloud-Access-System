from pydantic import BaseModel
from datetime import datetime

class UsageLogRead(BaseModel):
    id: int
    user_id: int
    api_name: str
    count: int
    timestamp: datetime

    class Config:
        from_attributes = True
