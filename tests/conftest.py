import pytest

from nested_diff_restful.api import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
