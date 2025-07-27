import pytest
from fastapi.testclient import TestClient

from app.db.engine import get_db
from main import app


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
