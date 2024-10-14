from datetime import datetime

from sqlalchemy import select, BigInteger, update, Text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

from ..modeles import AbstractModel


class Storage(AbstractModel):
    __tablename__ = 'storages'

    telegram_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    size_storage_byte: Mapped[int] = mapped_column(BigInteger(), default=None)
    size_files_byte: Mapped[int] = mapped_column(BigInteger(), default=None)


async def get_storage_by_dict_db(select_by: dict, session_maker: sessionmaker) -> Storage:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Storage).filter_by(**select_by)
            )
            return result.scalars().one()


async def get_storage_db(telegram_id: int, session_maker: sessionmaker) -> Storage:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Storage).where(Storage.telegram_id == telegram_id)
            )
            return result.scalars().one()


async def create_storage_db(telegram_id: int, session_maker: sessionmaker) -> [
    Storage, Exception]:
    async with session_maker() as session:
        async with session.begin():
            user = Storage(
                telegram_id=telegram_id,
                size_storage_byte=524288000,
                size_files_byte=0,
            )
            try:
                session.add(user)
                return Storage
            except ProgrammingError as _e:
                return _e


async def is_storage_exists_db(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(Storage).where(Storage.telegram_id == user_id))
            return bool(sql_res.first())


async def update_storage_db(telegram_id: int, data: dict, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(Storage).where(Storage.telegram_id == telegram_id).values(data))
            await session.commit()
