from datetime import datetime

from sqlalchemy import select, BigInteger, update, Text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

from ..modeles import AbstractModel


class File(AbstractModel):
    __tablename__ = 'files'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    destination: Mapped[str] = mapped_column(Text, default=None)
    size_byte: Mapped[int] = mapped_column(BigInteger(), default=None)
    date_upload: Mapped[datetime] = mapped_column()
    type: Mapped[str] = mapped_column(Text)


async def get_file_by_dict_db(select_by: dict, session_maker: sessionmaker) -> File:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(File).filter_by(**select_by)
            )
            return result.scalars().one()


async def create_file_db(telegram_id: int, destination: str, size_byte: int, type: str, session_maker: sessionmaker) -> [
    File, Exception]:
    async with session_maker() as session:
        async with session.begin():
            user = File(
                telegram_id=telegram_id,
                destination=destination,
                size_byte=size_byte,
                date_upload=datetime.now(),
                type=type
            )
            try:
                session.add(user)
                return File
            except ProgrammingError as _e:
                return _e


async def is_file_exists_db(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(File).where(File.telegram_id == user_id))
            return bool(sql_res.first())


async def update_file_db(telegram_id: int, data: dict, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(File).where(File.telegram_id == telegram_id).values(data))
            await session.commit()
