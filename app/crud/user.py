from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase[User]):

    async def get_user_by_login(
        self,
        login: str,
        session: AsyncSession
    ):
        result = await session.execute(
            select(User).where(
                User.is_active.is_(True),
                or_(User.email == login, User.phone == login)
            )
        )
        return result.scalar_one_or_none()


user_crud = CRUDUser(User)
