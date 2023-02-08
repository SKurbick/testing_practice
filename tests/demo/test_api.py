import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient

from demo.models import Message


@pytest.fixture
def message_factory():
    def factory(*args, **kwargs):
        return baker.make(Message, *args, **kwargs)

    return factory


@pytest.fixture
def user():
    return User.objects.create_user('admin')


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_get_messages(client, user, message_factory):
    # Arrange
    # Message.objects.create(user_id=user.id, text='test')
    messages = message_factory(_quantity=10)
    # Act
    response = client.get('/messages/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    #
    assert len(data) == len(messages)
    # assert data[0]['text'] == 'test'
    for i, m in enumerate(data):
        assert m['text'] == messages[i].text

@pytest.mark.django_db
def test_create_messages(client, user):
    count = Message.objects.count()
    response = client.post('/messages/', data={'user': user.id, 'text': 'test_text'})

    assert response.status_code == 201
    assert Message.objects.count() == count + 1
