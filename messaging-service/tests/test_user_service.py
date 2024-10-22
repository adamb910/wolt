import pytest
from unittest.mock import MagicMock

from repository.models.user import User

from services.user_service import get_users, create_user, update_user, delete_user


@pytest.fixture
def mock_session(monkeypatch):
    mock_session = MagicMock()

    monkeypatch.setattr('services.user_service.session', mock_session)

    return mock_session


def test_get_users_with_filter(mock_session):
    mock_user = User(id=1, name="John Doe", email="john@example.com")
    mock_session.query.return_value.filter_by.return_value.all.return_value = [mock_user]

    result = get_users(email_filter="john@example.com")

    mock_session.query.assert_called_once()
    mock_session.query.return_value.filter_by.assert_called_once_with(email="john@example.com")
    assert result == [mock_user]


def test_get_users_without_filter(mock_session):
    mock_user = User(id=1, name="John Doe", email="john@example.com")
    mock_session.query.return_value.all.return_value = [mock_user]

    result = get_users(email_filter=None)

    mock_session.query.assert_called_once()
    mock_session.query.return_value.all.assert_called_once()
    assert result == [mock_user]


def test_create_user(mock_session):
    mock_user = User(id=1, name="John Doe", email="john@example.com")
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    result = create_user(name="John Doe", email="john@example.com")

    mock_session.add.assert_called_once_with(result)
    mock_session.commit.assert_called_once()
    assert result.name == "John Doe"
    assert result.email == "john@example.com"


def test_update_user(mock_session):
    mock_user = User(id=1, name="John Doe", email="john@example.com")
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

    result = update_user(id=1, name="Jane Doe", email="jane@example.com")

    mock_session.query.assert_called_once()
    assert result.name == "Jane Doe"
    assert result.email == "jane@example.com"
    mock_session.commit.assert_called_once()


def test_delete_user(mock_session):
    mock_user = User(id=1, name="John Doe", email="john@example.com")
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

    delete_user(id=1)

    mock_session.delete.assert_called_once_with(mock_user)
    mock_session.commit.assert_called_once()
