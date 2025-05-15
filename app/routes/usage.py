from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload  # ✅ Required for eager loading
from app.database import get_async_session
from app.models.usage_log import UsageLog
from app.models.subscription import Subscription
from app.models.user import User
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.get("/usage/limit", summary="Check Limit For Current User")
async def check_limit_for_current_user(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    # ✅ Eager load the plan relationship
    result = await db.execute(
        select(Subscription)
        .options(selectinload(Subscription.plan))
        .where(Subscription.user_id == user.id)
    )
    subscription = result.scalars().first()

    if not subscription or not subscription.plan:
        raise HTTPException(status_code=404, detail="No active subscription or plan found")

    plan = subscription.plan
    allowed_limits = plan.usage_limits

    usage_result = await db.execute(
        select(UsageLog).where(UsageLog.user_id == user.id)
    )
    usage_logs = usage_result.scalars().all()

    usage_summary = {}
    for log in usage_logs:
        usage_summary[log.api_name] = usage_summary.get(log.api_name, 0) + log.count

    report = []
    for api, allowed in allowed_limits.items():
        used = usage_summary.get(api, 0)
        status = "Within Limit" if used < allowed else "Limit Exceeded"
        report.append({
            "api": api,
            "used": used,
            "allowed": allowed,
            "status": status
        })

    return {"user_id": user.id, "usage_report": report}
