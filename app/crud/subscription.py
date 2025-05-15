from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models
from ..schemas.subscription import SubscriptionCreate

async def create_subscription(db: AsyncSession, subscription: SubscriptionCreate):
    user = await db.execute(select(models.User).where(models.User.id == subscription.user_id))
    if user.scalar() is None:
        raise HTTPException(status_code=404, detail="User not found")

    plan = await db.execute(select(models.Plan).where(models.Plan.id == subscription.plan_id))
    if plan.scalar() is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    db_subscription = models.Subscription(**subscription.dict())
    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription)
    return db_subscription

async def get_all_subscriptions(db: AsyncSession):
    result = await db.execute(select(models.Subscription))
    return result.scalars().all()
