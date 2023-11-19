from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Database:
    def __init__(self, url: str) -> None:
        self._engine = create_async_engine(url)
        self.session_factory = async_scoped_session(
            session_factory=sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )
