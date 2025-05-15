from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.subscription import Subscription
from app.models.user import User
from app.models.plan import Plan
from app.database import get_async_session
from app.schemas.subscription import SubscriptionCreate
from app.utils.dependencies import require_admin

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

# ✅ Admin assigns or updates a user's subscription
@router.put("/{user_id}")
async def assign_or_update_subscription(
    user_id: int,
    subscription_data: SubscriptionCreate,
    db: AsyncSession = Depends(get_async_session),
    admin: User = Depends(require_admin)
):
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plan_result = await db.execute(select(Plan).where(Plan.id == subscription_data.plan_id))
    plan = plan_result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    subscription_result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    subscription = subscription_result.scalars().first()

    if subscription:
        subscription.plan_id = subscription_data.plan_id
    else:
        subscription = Subscription(user_id=user_id, plan_id=subscription_data.plan_id)
        db.add(subscription)

    await db.commit()
    await db.refresh(subscription)

    return {
        "detail": "Subscription updated",
        "subscription": {
            "user_id": subscription.user_id,
            "plan_id": subscription.plan_id
        }
    }
