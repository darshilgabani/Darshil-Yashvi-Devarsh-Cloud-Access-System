from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.utils.dependencies import require_admin
from app.database import get_async_session
from app.models.plan import Plan

router = APIRouter()

@router.put("/admin/update-plan/{plan_id}")
async def update_plan_limits(
    plan_id: int,
    db: AsyncSession = Depends(get_async_session),
    admin_user = Depends(require_admin)
):
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalars().first()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Update limits
    plan.usage_limits = {
        "api1": 100,
        "api2": 100,
        "api3": 50,
        "api4": 50,
        "api5": 20,
        "api6": 20
    }

    await db.commit()
    await db.refresh(plan)
    return {"message": "Plan usage limits updated", "updated_limits": plan.usage_limits}

@router.get("/admin/dashboard")
async def admin_dashboard(admin_user = Depends(require_admin)):
    return {"message": f"Welcome Admin {admin_user.username}"}
