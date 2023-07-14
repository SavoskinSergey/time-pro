import pytest

from core.fixtures.account import user
from core.task.models import Task


@pytest.fixture
def task(db, user):
    return Task.objects.create(
        author=user,
        title='Task1',
        description='Test Description',
        amount=10
        )
