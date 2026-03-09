from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession):
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, session: AsyncSession, id: int):
        return await cls.find_one(session, id=id)

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        obj = cls.model(**values)

        session.add(obj)
        await session.commit()
        await session.refresh(obj)

        return obj

    @classmethod
    async def update(cls, session: AsyncSession, filter_by: dict, values: dict):
        stmt = (
            update(cls.model)
            .filter_by(**filter_by)
            .values(**values)
            .returning(cls.model)
        )

        result = await session.execute(stmt)

        await session.commit()

        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by):
        obj = await cls.find_one(session, **filter_by)

        if obj:
            await session.delete(obj)
            await session.commit()

    @classmethod
    async def bulk_create(cls, session: AsyncSession, values: list[dict]):
        stmt = insert(cls.model)

        await session.execute(stmt, values)

        await session.commit()