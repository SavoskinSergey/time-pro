import pytest
from core.account.models import User

data_user = {
    "username": "test_user",
    "email": "test@mail.ru",
    "first_name": "Test",
    "last_name": "User",
    "password": "test_password",
    "phone_number": "+79048764325"
}


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(**data_user)
