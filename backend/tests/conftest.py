import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from app.core.config import settings
from app.core.database import db_instance
from app.services.interview_service import _in_memory_sessions
from app.services.auth_service import _in_memory_users
from app.services.resume_service import _in_memory_resumes
from app.main import app

TEST_DB_NAME = "accesshire_test_db"

def _sync_clean_test_db():
    try:
        sync_client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        test_db = sync_client[TEST_DB_NAME]
        test_db.interview_sessions.delete_many({})
        test_db.users.delete_many({})
        test_db.resumes.delete_many({})
        sync_client.close()
    except Exception:
        pass

@pytest.fixture(scope="session", autouse=True)
def configure_test_environment():
    """
    Points database name to isolated test database for automated tests.
    Ensures production Atlas database (accesshire_db) is never touched by tests.
    Drops the test database upon test session completion.
    """
    original_db_name = settings.DATABASE_NAME
    settings.DATABASE_NAME = TEST_DB_NAME
    _sync_clean_test_db()
    yield
    settings.DATABASE_NAME = original_db_name
    # Drop the isolated test database after all tests complete
    try:
        sync_client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        sync_client.drop_database(TEST_DB_NAME)
        sync_client.close()
    except Exception:
        pass

@pytest.fixture
def client():
    """
    Yields FastAPI test client configured against the isolated test database.
    Cleans up all test collections before and after each test synchronously.
    """
    _in_memory_sessions.clear()
    _in_memory_users.clear()
    _in_memory_resumes.clear()
    _sync_clean_test_db()

    with TestClient(app) as c:
        if db_instance.client is not None:
            db_instance.db = db_instance.client[TEST_DB_NAME]

        yield c

        _sync_clean_test_db()
        _in_memory_sessions.clear()
        _in_memory_users.clear()
        _in_memory_resumes.clear()
