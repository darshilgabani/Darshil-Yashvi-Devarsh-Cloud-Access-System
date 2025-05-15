from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from ..crud.user import create_user, get_all_users
from ..schemas.user import UserCreate, UserRead
from ..utils.auth import get_current_user  

router = APIRouter()

@router.post("/users/", response_model=UserRead)
async def create(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        return await create_user(db, user)
    except Exception as e:
        print("ERROR CREATING USER:", e)
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.get("/users/", response_model=list[UserRead])
async def read_users(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user)  
):
    return await get_all_users(db)

