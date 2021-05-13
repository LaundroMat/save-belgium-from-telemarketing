import pytest
from faker import Faker
from app import create_app

fake = Faker()


@pytest.fixture
def app():
    return create_app()
