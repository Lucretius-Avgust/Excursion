from http import HTTPStatus

from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user_crud


async def check_object_by_id(
    crud: Any,
    obj_id: UUID,
    session: AsyncSession,
) -> Any:
    """Универсальная проверка существования объекта по ID."""
    obj = await crud.get(
            obj_id=obj_id,
            session=session,
        )
    if obj is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='По такому id не чего не нашлось.',
        )
    return obj


async def check_objects(
    crud: Any,
    session: AsyncSession,
) -> Any:
    """Универсальная проверка есть ли хоть один объект."""
    objs = await crud.get_all(
        session=session
    )
    if not objs:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Нет ни одного объекта.',
        )
    return objs


async def check_create_user(
    login: str,
    session: AsyncSession,
) -> Any:

    login_check = await user_crud.get_user_by_login(
        login=login,
        session=session
    )
    if login_check:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Пользователь с таким логином существует.'
        )


async def check_update_user_login(
    user_id: UUID,
    login: str | None,
    session: AsyncSession,
) -> None:
    """Проверяет, что email/phone не заняты другим пользователем."""

    if login is None:
        return

    existing_user = await user_crud.get_user_by_login(
        login=login,
        session=session
    )

    if existing_user and existing_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Этот логин уже используется другим пользователем."
        )
