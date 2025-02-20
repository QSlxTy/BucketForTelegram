import sqlalchemy.ext.asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

from integrations.database.models.file import File
from integrations.database.models.storage import Storage
from integrations.database.models.user import User
from src.config import conf


def get_session_maker(engine: sqlalchemy.ext.asyncio.AsyncEngine) -> sessionmaker:
    """
    :param engine:
    :return:
    """
    return sessionmaker(engine, class_=sqlalchemy.ext.asyncio.AsyncSession, expire_on_commit=False)


async def create_connection() -> sqlalchemy.ext.asyncio.AsyncEngine:
    url = conf.db.build_connection_str()

    engine = _create_async_engine(
        url=url, pool_pre_ping=True)
    return engine


class Database:
    def __init__(
            self,
            session: AsyncSession,
            user: User = None,
            file: File = None,
            storage: Storage = None

    ):
        self.session = session
        self.user = user or User()
        self.file = file or File()
        self.storage = storage or Storage()




async def init_models(engine):
    """
    initialize(create) models of database
    :param engine:
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(File.metadata.create_all)
        await conn.run_sync(Storage.metadata.create_all)

