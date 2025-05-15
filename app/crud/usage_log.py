from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from ..models.usage_log import UsageLog
from ..models.user import User

async def log_api_usage(db: AsyncSession, user_id: int, api_name: str):
    log = UsageLog(user_id=user_id, api_name=api_name)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

async def count_usage(db: AsyncSession, user_id: int, api_name: str):
    result = await db.execute(
        select(UsageLog).where(
            UsageLog.user_id == user_id,
            UsageLog.api_name == api_name,
            UsageLog.timestamp >= datetime.utcnow().replace(hour=0, minute=0, second=0)  # today
        )
    )
    return result.scalars().all()
