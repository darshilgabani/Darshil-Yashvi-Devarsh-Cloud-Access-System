from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..utils.dependencies import require_admin
from ..schemas.permission import PermissionCreate, PermissionUpdate, PermissionOut
from ..crud.permission import create_permission, update_permission, delete_permission
from ..database import get_async_session

router = APIRouter(prefix="/permission", tags=["Permission"])

# ✅ Modified to accept a list of permissions
@router.post("/", response_model=List[PermissionOut])
async def add_permissions(
    permissions: List[PermissionCreate],
    db: AsyncSession = Depends(get_async_session),
    admin_user=Depends(require_admin)
):
    created_permissions = []
    for perm in permissions:
        new_permission = await create_permission(db, perm)
        created_permissions.append(new_permission)
    return created_permissions

@router.put("/{permission_id}", response_model=PermissionOut)
async def modify_permission(
    permission_id: int,
    permission: PermissionUpdate,
    db: AsyncSession = Depends(get_async_session),
    admin_user=Depends(require_admin)
):
    return await update_permission(db, permission_id, permission)

@router.delete("/{permission_id}")
async def remove_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_async_session),
    admin_user=Depends(require_admin)
):
    return await delete_permission(db, permission_id)
