import pytest

from app.app import create_app


@pytest.fixture
def client():
    with create_app().test_client() as client:
        yield client
