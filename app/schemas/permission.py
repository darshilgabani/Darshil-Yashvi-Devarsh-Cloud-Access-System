from pydantic import BaseModel

class PermissionCreate(BaseModel):
    name: str
    endpoint: str
    description: str

class PermissionUpdate(BaseModel):
    name: str
    endpoint: str
    description: str

class PermissionOut(PermissionCreate):
    id: int

    class Config:
        from_attributes = True
