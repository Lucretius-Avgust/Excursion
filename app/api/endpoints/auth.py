from fastapi import (
    APIRouter, Depends, Form,
    HTTPException, status, Response,
    Cookie
)
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.core.db import get_async_session
from app.crud.user import user_crud
from app.services.auth_service import (
    create_access_token, create_refresh_token,
    verify_password
)
from app.core.constants import SECRET_KEY, ALGORITHM
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    login: str = Form(...),
    password: str = Form(...),
):
    user: User | None = await user_crud.get_user_by_login(login, session)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Юзер не активен"
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 30,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
async def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
):
    if refresh_token is None:
        raise HTTPException(
            status_code=401, detail="Отсутствует токен обновления"
        )

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401, detail="Неверный тип токена"
            )
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Неверный токен обновления"
        )

    user_id = payload.get("sub")

    new_access = create_access_token({"sub": user_id})
    new_refresh = create_refresh_token({"sub": user_id})

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 30,
    )

    return {"access_token": new_access, "token_type": "bearer"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"detail": "Вышел из системы"}
