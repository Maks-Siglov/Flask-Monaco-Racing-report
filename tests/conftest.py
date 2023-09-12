import pytest
from myapp import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        return client
