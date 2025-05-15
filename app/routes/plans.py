from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_session
from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanRead
from app.utils.dependencies import require_admin

router = APIRouter()

# Existing: Create plan
@router.post("/plans", response_model=PlanRead)
async def create_plan(plan: PlanCreate, db: AsyncSession = Depends(get_async_session), admin=Depends(require_admin)):
    new_plan = Plan(**plan.dict())
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan

# ✅ Update plan
@router.put("/plans/{plan_id}", response_model=PlanRead)
async def update_plan(plan_id: int, updated_plan: PlanCreate, db: AsyncSession = Depends(get_async_session), admin=Depends(require_admin)):
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    for attr, value in updated_plan.dict().items():
        setattr(plan, attr, value)

    await db.commit()
    await db.refresh(plan)
    return plan

# ✅ Delete plan
@router.delete("/plans/{plan_id}")
async def delete_plan(plan_id: int, db: AsyncSession = Depends(get_async_session), admin=Depends(require_admin)):
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    await db.delete(plan)
    await db.commit()
    return {"detail": "Plan deleted successfully"}
