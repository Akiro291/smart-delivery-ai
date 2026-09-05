"""
Users endpoints with role management.
"""


from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user, require_role
from app.core.database import get_async_session
from app.db.models.user import RoleRequest, RoleRequestStatus, UserRole
from app.db.models.user import User as UserModel
from app.repositories.user_repo import (
    activate_user,
    create_role_notification,
    create_role_request,
    create_user,
    deactivate_user,
    get_admin_users,
    get_all_users,
    get_role_request_by_user,
    get_role_requests,
    get_user_by_email,
    get_user_by_id,
    get_user_count,
    get_user_count_by_role,
    get_users_by_role,
    update_role_request,
    update_user_role,
)
from app.schemas.user import (
    RoleRequest as RoleRequestSchema,
)
from app.schemas.user import (
    RoleRequestCreate,
    RoleRequestWithUser,
    UserCreate,
    UserUpdateRole,
    UserUpdateUserStatus,
)
from app.schemas.user import (
    User as UserSchema,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_async_session),
):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user.role = UserRole.CUSTOMER
    new_user = await create_user(db, user)
    return new_user


@router.get("/", response_model=list[UserSchema])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    role: str | None = Query(None),
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_role(["ADMIN"])),
):
    if role:
        users = await get_users_by_role(db, role, skip, limit)
    else:
        users = await get_all_users(db, skip, limit)
    return users


@router.get("/count", response_model=dict)
async def get_users_count(
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_role(["ADMIN"])),
):
    total = await get_user_count(db)
    customers = await get_user_count_by_role(db, "CUSTOMER")
    couriers = await get_user_count_by_role(db, "COURIER")
    admins = await get_user_count_by_role(db, "ADMIN")
    return {
        "total": total,
        "customers": customers,
        "couriers": couriers,
        "admins": admins,
    }





@router.post("/role-request", response_model=RoleRequestSchema)
async def request_role_change(
    request_data: RoleRequestCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin users cannot request role changes",
        )
    if request_data.requested_role == current_user.role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have this role",
        )

    existing = await get_role_request_by_user(db, current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have a pending role request",
        )

    role_request = await create_role_request(db, current_user.id, request_data.requested_role.name, request_data.reason)

    # Send notifications to all admins
    admins = await get_admin_users(db)
    role_name = request_data.requested_role
    for admin in admins:
        user_name = current_user.full_name or current_user.email
        await create_role_notification(
            db,
            admin.id,
            title=f"Заявка на роль {role_name.lower()}",
            message=f"Пользователь {user_name} запросил роль {role_name.lower()}. Причина: {request_data.reason or 'Не указана'}",
        )

    return role_request


@router.get("/role-requests", response_model=list[RoleRequestWithUser])
async def list_role_requests(
    status_filter: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_role(["ADMIN"])),
):
    requests = await get_role_requests(db, status_filter, skip, limit)
    result = []
    for req in requests:
        user = await get_user_by_id(db, req.user_id)
        result.append(
            RoleRequestWithUser(
                id=req.id,
                user_id=req.user_id,
                requested_role=req.requested_role,
                status=req.status,
                reason=req.reason,
                reviewed_by=req.reviewed_by,
                reviewed_at=req.reviewed_at,
                created_at=req.created_at,
                user_email=user.email if user else None,
                user_full_name=user.full_name if user else None,
            )
        )
    return result


@router.put("/role-requests/{request_id}/approve", response_model=RoleRequestSchema)
async def approve_role_request(
    request_id: int,
    reason: str | None = Query(None),
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_role(["ADMIN"])),
):
    result = await db.execute(select(RoleRequest).where(RoleRequest.id == request_id))
    role_request = result.scalar_one_or_none()
    if not role_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role request not found",
        )
    if role_request.status != RoleRequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request is not pending",
        )

    user = await get_user_by_id(db, role_request.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.role = role_request.requested_role
    await db.commit()
    role_request = await update_role_request(db, role_request, "APPROVED", current_user.id, reason)
    return role_request


@router.put("/role-requests/{request_id}/reject", response_model=RoleRequestSchema)
async def reject_role_request(
    request_id: int,
    reason: str | None = Query(None),
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_role(["ADMIN"])),
):
    result = await db.execute(select(RoleRequest).where(RoleRequest.id == request_id))
    role_request = result.scalar_one_or_none()
    if not role_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role request not found",
        )
    if role_request.status != RoleRequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request is not pending",
        )

    role_request = await update_role_request(db, role_request, "REJECTED", current_user.id, reason)
    return role_request


@router.get("/me/role-request", response_model=RoleRequestSchema | None)
async def get_my_role_request(
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    return await get_role_request_by_user(db, current_user.id)
@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user),
):
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put("/{user_id}/role", response_model=UserSchema)
async def change_user_role(
    user_id: int,
    role_data: UserUpdateRole,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_role(["ADMIN"])),
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role",
        )
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if role_data.role == UserRole.ADMIN and user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already admin",
        )
    user = await update_user_role(db, user, role_data.role.name)
    return user


@router.put("/{user_id}/status", response_model=UserSchema)
async def toggle_user_status(
    user_id: int,
    status_data: UserUpdateUserStatus,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_role(["ADMIN"])),
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own status",
        )
    user = await get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if status_data.is_active:
        user = await activate_user(db, user_id)
    else:
        await deactivate_user(db, user_id)
        user = await get_user_by_id(db, user_id=user_id)
    return user
