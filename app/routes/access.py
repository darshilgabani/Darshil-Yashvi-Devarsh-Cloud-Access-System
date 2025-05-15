from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_session
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.user import User
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.get("/access/{api_name}")
async def check_access(api_name: str, db: AsyncSession = Depends(get_async_session), user: User = Depends(get_current_user)):
    result = await db.execute(select(Subscription).where(Subscription.user_id == user.id))
    subscription = result.scalars().first()

    if not subscription:
        raise HTTPException(status_code=403, detail="No active subscription")

    plan = subscription.plan
    if api_name not in plan.api_permissions:
        raise HTTPException(status_code=403, detail=f"Access to {api_name} is not allowed")

    return {"message": f"Access granted to {api_name}"}
