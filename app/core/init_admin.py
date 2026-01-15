import asyncio
from sqlalchemy import select
from passlib.context import CryptContext

from app.core.db import get_async_session
from app.models import User, UserRole
from app.core.config import settings
import logging


logger = logging.getLogger(__name__)
logger.info("Создаём первого администратора...")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_first_admin():
    async with get_async_session() as session:
        result = await session.execute(
            select(User).where(User.role == UserRole.ADMIN)
        )
        admin = result.scalar_one_or_none()

        if admin:
            logger.warning("Админ уже существует:", admin.email)
            return

        if (
            not settings.first_superuser_email
            or not settings.first_superuser_password
        ):
            logger.warning("Нет данных для суперпользователя в .env")
            return

        hashed_password = pwd_context.hash(
            settings.first_superuser_password.get_secret_value()
        )

        admin = User(
            username=settings.first_superuser_username or "admin",
            email=settings.first_superuser_email,
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            is_active=True,
        )
        session.add(admin)
        await session.commit()
        logger.info("Создан первый админ:", admin.email)


if __name__ == "__main__":
    asyncio.run(create_first_admin())