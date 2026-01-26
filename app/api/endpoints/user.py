from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.dependencies import GuideOrAdmin, CurrentUser, SessionDep
from app.shemas.user import UserCreate, UserRead, UserUpdate
from app.api.validators import (
    check_object_by_id,
    check_objects,
    check_create_user,
    check_update_user_login
)
from app.crud import user_crud
from app.models.user import User, UserRole
from app.services.auth_service import hash_password


router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "/{user_id}",
    response_model=UserRead
)
async def get_user_by_id(
    current_user: CurrentUser,
    session: SessionDep,
    user_id: UUID
) -> User:
    if current_user.id != user_id and current_user.role not in (UserRole.ADMIN, UserRole.GUIDE):
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    result = await check_object_by_id(
        crud=user_crud,
        session=session,
        obj_id=user_id,
    )
    return result


@router.get(
    "/",
    response_model=list[UserRead]
)
async def get_user_all(
    _: GuideOrAdmin,
    session: SessionDep
):
    results = await check_objects(
        crud=user_crud,
        session=session
    )
    return results


@router.post(
    "/",
    response_model=UserRead,
    response_model_exclude_none=True,
    summary='Регистрация',
)
async def create_user(
    user: UserCreate,
    session: SessionDep
):
    await check_create_user(
        login=user.email or user.phone,
        session=session
    )
    new_user = await user_crud.create(
        obj_in=user,
        session=session,
        extra_fields={
            'hashed_password': hash_password(user.password),
            'role': UserRole.CUSTOMER,
            'is_active': True
        },
    )
    return new_user


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    response_model_exclude_none=True,
)
async def udpade_user(
    user_id: UUID,
    obj_in: UserUpdate,
    session: SessionDep
):
    user = await check_object_by_id(
        crud=user_crud,
        obj_id=user_id,
        session=session
    )
    login = obj_in.email or obj_in.phone
    await check_update_user_login(
        user_id=user_id,
        login=login,
        session=session
    )
    updated_user = await user_crud.update(
        db_obj=user,
        obj_in=obj_in,
        session=session
    )
    return updated_user
