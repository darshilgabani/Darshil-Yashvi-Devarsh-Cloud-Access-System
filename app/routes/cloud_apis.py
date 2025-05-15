from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database import get_async_session
from app.models import User, Plan, Subscription, UsageLog

router = APIRouter(prefix="/cloud", tags=["Services"])

# ✅ Helper to check permission + usage
def check_permission_and_usage(plan: Plan, api: str, usage_logs: List[UsageLog]):
    if api not in plan.api_permissions:
        raise HTTPException(status_code=403, detail=f"Access denied to {api}")
    
    used_count = sum(log.count for log in usage_logs if log.api_name == api)
    allowed = plan.usage_limits.get(api, 0)

    if used_count >= allowed:
        raise HTTPException(status_code=403, detail=f"Usage limit exceeded for {api}")

    return used_count, allowed

# ✅ Main logic to access the API
async def access_cloud_api(user_id: int, api: str, db: AsyncSession):
    # Verify user exists
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get subscription and plan
    result = await db.execute(
        select(Subscription).options(selectinload(Subscription.plan)).where(Subscription.user_id == user_id)
    )
    subscription = result.scalars().first()
    if not subscription or not subscription.plan:
        raise HTTPException(status_code=404, detail="Subscription or plan not found")

    plan = subscription.plan

    # Get usage logs
    usage_result = await db.execute(
        select(UsageLog).where(
            UsageLog.user_id == user_id,
            UsageLog.api_name == api
        )
    )
    logs = usage_result.scalars().all()

    # Check access
    used_count, allowed = check_permission_and_usage(plan, api, logs)

    # Record usage
    usage_log = UsageLog(user_id=user_id, api_name=api, count=1)
    db.add(usage_log)
    await db.commit()

    return {
        "user": user.username,
        "message": f"{api} accessed successfully",
        "used": used_count + 1,
        "allowed": allowed
    }

# ✅ Cloud API endpoints
api_names = [
    "/users/",
    "/plans",
    "/subscriptions",
    "/token",
    "/usage/limit",
    "/permissions"
]

# ✅ Create one route per API, with user_id
def create_cloud_api_route(api_name: str):
    async def handler(
        user_id: int,
        db: AsyncSession = Depends(get_async_session),
    ):
        return await access_cloud_api(user_id, api_name, db)

    path = f"{api_name.rstrip('/')}/{{user_id}}"
    router.add_api_route(path, handler, methods=["GET"], summary=f"Access {api_name.upper()}")

# ✅ Register all routes
for api in api_names:
    create_cloud_api_route(api)
