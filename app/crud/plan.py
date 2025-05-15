from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.plan import Plan
from ..schemas.plan import PlanCreate

async def create_plan(plan: PlanCreate, db: AsyncSession):
    new_plan = Plan(
        name=plan.name,
        description=plan.description,
        api_permissions=plan.api_permissions,
        usage_limits=plan.usage_limits
    )
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan

async def get_all_plans(db: AsyncSession):
    result = await db.execute(select(Plan))
    return result.scalars().all()
