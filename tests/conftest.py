import pytest

from fastapi.testclient import TestClient
from src.main import app
from src.routes.jokes import jokes


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as test_client:
        yield test_client

