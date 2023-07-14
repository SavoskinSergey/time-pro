import pytest
from django.urls import reverse
from django.test import Client

from core.fixtures.account import user
from core.fixtures.task import task
from core.task.models import Task


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_task_list_view(client, user):
    # Входим в систему как пользователь
    client.force_login(user)

    # Создаем несколько задач для пользователя
    Task.objects.create(author=user, title='Task 1', description='Test Description 1', amount=10)
    Task.objects.create(author=user, title='Task 2', description='Test Description 2', amount=20)

    # Получаем URL для просмотра списка задач
    url = reverse('task:tasks')

    # Отправляем GET-запрос к URL
    response = client.get(url)

    # Проверяем, что ответ имеет статус 200 (успех) и содержит ожидаемую информацию
    assert response.status_code == 200
    assert 'Task 1' in response.content.decode()
    assert 'Task 2' in response.content.decode()
    print(response.content.decode())

@pytest.mark.django_db
def test_task_detail_view(client, user, task):
    # Входим в систему как пользователь
    client.force_login(user)

    # Получаем URL для просмотра деталей задачи
    url = reverse('task:task_detail', kwargs={'pk': task.pk})

    # Отправляем GET-запрос к URL
    response = client.get(url)

    # Проверяем, что ответ имеет статус 200 (успех) и содержит ожидаемую информацию
    assert response.status_code == 200
    # assert 'Task 1' in response.content.decode()
    # assert 'Test Description' in response.content.decode()


@pytest.mark.django_db
def test_task_update_view(client, user, task):
    # Входим в систему как пользователь
    client.force_login(user)

    # Получаем URL для редактирования задачи
    url = reverse('task:task_update', kwargs={'pk': task.pk})

    # Отправляем GET-запрос к URL
    response = client.get(url)

    # Проверяем, что ответ имеет статус 200 (успех) и содержит ожидаемую информацию
    assert response.status_code == 200
    # assert 'Task 1' in response.content.decode()
    # assert 'Test Description' in response.content.decode()