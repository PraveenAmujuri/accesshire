import asyncio
import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.database import db_instance
from app.services.interview_service import _in_memory_sessions
from app.main import app

TEST_DB_NAME = "accesshire_test_db"

@pytest.fixture(scope="session", autouse=True)
def configure_test_environment():
    """
    Points database name to isolated test database for automated tests.
    Ensures production Atlas database (accesshire_db) is never touched by tests.
    Drops the test database upon test session completion.
    """
    original_db_name = settings.DATABASE_NAME
    settings.DATABASE_NAME = TEST_DB_NAME
    yield
    settings.DATABASE_NAME = original_db_name
    # Drop the isolated test database after all tests complete
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        async def drop():
            await client.drop_database(TEST_DB_NAME)
            client.close()
        asyncio.run(drop())
    except Exception:
        pass

@pytest.fixture
def client():
    """
    Yields FastAPI test client configured against the isolated test database.
    Cleans up all test documents before and after each test while the database connection is live.
    """
    _in_memory_sessions.clear()
    with TestClient(app) as c:
        if db_instance.client is not None:
            db_instance.db = db_instance.client[TEST_DB_NAME]
            try:
                asyncio.run(db_instance.db.interview_sessions.delete_many({}))
            except Exception:
                pass

        yield c

        # Teardown: clean up test documents before lifespan terminates the connection
        if db_instance.client is not None and db_instance.db is not None:
            try:
                asyncio.run(db_instance.db.interview_sessions.delete_many({}))
            except Exception:
                pass
        _in_memory_sessions.clear()
