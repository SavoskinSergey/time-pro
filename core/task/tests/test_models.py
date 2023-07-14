import pytest

from core.fixtures.account import user
from core.task.models import Task



@pytest.mark.django_db
def test_create_task(user):
    task = Task.objects.create(
        author=user,
        title='Task1',
        description='Test Description',
        amount=10
        )
    assert task.title == 'Task1'
    assert task.author == user
    assert task.description == 'Test Description'
    assert task.amount == 10
    assert task.charge == 0
    assert task.status == 'new'
    assert task.parent is None
    assert Task.objects.count() == 1
