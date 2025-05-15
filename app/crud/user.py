from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import UserCreate
from ..models.user import User
from ..utils.auth import get_password_hash  # ✅ import hashing function

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)  # ✅ hash the password
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()
