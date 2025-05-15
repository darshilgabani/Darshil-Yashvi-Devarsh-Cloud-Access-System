from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./cloudaccess.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

# Dependency for routes
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Auto-create all tables
async def create_db_and_tables():
    from app.models.user import User
    from app.models.plan import Plan
    from app.models.subscription import Subscription
    from app.models.usage_log import UsageLog
    from app.models.permission import Permission  # ✅ include this

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
