from uncoupledetl.data_types import Base
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
)
from uncoupledetl.variables import LOCAL_DATABASE
from sqlalchemy.orm import sessionmaker


class Loader:
    def __init__(self, data: object):
        self.data = data

    async def load_strategy(self, load_strategy):
        return await load_strategy(self.data)


async def create_database(engine: AsyncEngine) -> None:
    """Drop the existing metabase and creates a new one in its place.

    Args:
        engine (AsyncEngine): The engine to use to connect with the database.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def load_to_local_database(data: object):
    """Load the data to the local database.

    Args:
        data (object): The data to load.
    """
    engine = create_async_engine(LOCAL_DATABASE)
    await create_database(engine)
    session = sessionmaker(engine, future=True, class_=AsyncSession)
    async with session() as s:
        s.add_all(data)
        await s.commit()
