from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from pydantic import BaseModel


ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(
        self, model: Type[ModelType]
    ):
        self.model = model

    async def get(
        self,
        session: AsyncSession,
        obj_id: int
    ) -> Optional[ModelType]:
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        obj_in: BaseModel,
        extra_fields: Optional[dict[str, Any]] = None,
    ) -> ModelType:
        obj_data = obj_in.model_dump()

        if extra_fields:
            obj_data.update(extra_fields)

        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: BaseModel,
        session: AsyncSession,
    ) -> ModelType:
        """Обновить существующий объект."""
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
