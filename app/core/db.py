from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from uuid import UUID

from app.core.config import settings
from app.core.constants import UUID_LEN

class PreBase:
    """
    Базовый класс для всех ORM-моделей.

    Автоматически задаёт имя таблицы на основе имени класса,
    и добавляет поле `id` как первичный ключ.
    """

    @declared_attr
    def __tablename__(cls):
        """Генерирует имя таблицы, равное имени класса."""
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(
        String(UUID_LEN),
        primary_key=True,
        default=lambda: str(uuid4()),
        unique=True,
        nullable=False,
    )



Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.db_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """
    Зависимость FastAPI для получения асинхронной сессии.

    Используется в обработчиках (роутах) для доступа к базе данных.
    """
    print("DB URL:", settings.db_url)
    async with AsyncSessionLocal() as async_session:
        yield async_session
