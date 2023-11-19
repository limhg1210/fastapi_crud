import asyncio

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config.settings import get_settings
from main import create_app


test_app = create_app(env_name="test")
settings = get_settings(env_name="test")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(test_app):
        async with AsyncClient(app=test_app, base_url="http://testserver") as test_client:
            yield test_client


@pytest.fixture(scope="session")
def session_factory():
    engine = create_engine(
        f"mysql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
        f"@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}"
    )
    yield scoped_session(sessionmaker(bind=engine))
