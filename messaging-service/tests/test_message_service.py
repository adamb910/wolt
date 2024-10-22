import pytest
from unittest.mock import MagicMock

from datetime import datetime

from repository.models.user import User
from repository.models.message import Message

from services.message_service import create_message, delete_message, get_messages_from_user


@pytest.fixture
def mock_session(monkeypatch):
    mock_session = MagicMock()
    mock_engine = MagicMock()

    monkeypatch.setattr('repository.engine.engine', mock_engine)
    monkeypatch.setattr('services.message_service.session', mock_session)

    return mock_session


def test_create_message(mock_session):
    current_timestamp = str(int(datetime.utcnow().timestamp()))
    mock_user = User(id="1", name="Test User")
    mock_message = Message(text="Hello", sender=mock_user, timestamp=current_timestamp)
    
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    
    result = create_message(text="Hello", user_id="1")
    
    mock_session.query.assert_called_once()
    mock_session.add.assert_called_once_with(result)
    mock_session.commit.assert_called_once()
    
    assert result.text == "Hello"
    assert result.sender == mock_user
    assert result.timestamp == current_timestamp


def test_delete_message(mock_session):
    mock_message = Message(id="1", text="Hello", user_id="1", timestamp="1625000000")
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_message

    delete_message(id="1")
    mock_session.delete.assert_called_once_with(mock_message)
    mock_session.commit.assert_called_once()


def test_delete_message_not_found(mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    delete_message(id="1")
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()


def test_get_messages_from_user(mock_session):
    mock_message_1 = Message(id="1", text="Hello", user_id="1", timestamp="1625000000")
    mock_message_2 = Message(id="2", text="World", user_id="1", timestamp="1625001000")
    mock_session.query.return_value.filter_by.return_value.all.return_value = [mock_message_1, mock_message_2]

    result = get_messages_from_user(user_id="1")
    mock_session.query.assert_called_once()
    assert len(result) == 2
    assert result[0].text == "Hello"
    assert result[1].text == "World"


def test_get_messages_from_user_empty(mock_session):
    mock_session.query.return_value.filter_by.return_value.all.return_value = []

    result = get_messages_from_user(user_id="1")
    mock_session.query.assert_called_once()
    assert result == []


def test_create_message_with_invalid_user(mock_session):
    mock_session.add.side_effect = ValueError("Invalid user")
    
    with pytest.raises(ValueError, match="Invalid user"):
        create_message(text="Invalid", user_id="999")
