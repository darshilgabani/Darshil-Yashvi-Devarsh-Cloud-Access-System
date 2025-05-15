from pydantic import BaseModel
from typing import Optional

class SubscriptionCreate(BaseModel):
    user_id: int
    plan_id: int

class SubscriptionRead(BaseModel):
    id: int
    user_id: int
    plan_id: int

    class Config:
        from_attributes = True



