from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from ..models.permission import Permission
from ..schemas.permission import PermissionCreate, PermissionUpdate

async def create_permission(db: AsyncSession, permission: PermissionCreate):
    new_permission = Permission(**permission.dict())
    db.add(new_permission)
    await db.commit()
    await db.refresh(new_permission)
    return new_permission

async def update_permission(db: AsyncSession, permission_id: int, permission: PermissionUpdate):
    result = await db.execute(select(Permission).where(Permission.id == permission_id))
    db_permission = result.scalars().first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    for field, value in permission.dict().items():
        setattr(db_permission, field, value)
    
    await db.commit()
    await db.refresh(db_permission)
    return db_permission

async def delete_permission(db: AsyncSession, permission_id: int):
    result = await db.execute(select(Permission).where(Permission.id == permission_id))
    db_permission = result.scalars().first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    await db.delete(db_permission)
    await db.commit()
    return {"message": "Permission deleted"}
