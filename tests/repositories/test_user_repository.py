from unittest import mock
import pytest
from src.models.sqlite.entities.user import User
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.repositories.user_repository import UserRepository

class MockConnection:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(User)],
                    [User(username="Maria", password="123", role="user"), User(username="Manuel", password="abc", role="user")]
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): pass

def test_create_user():
    mock_connection = MockConnection()
    user_repository = UserRepository(mock_connection)

    user_repository.create_user(username="José", password="123", role="user")

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_error_create_user():
    mock_connection = MockConnection()
    mock_connection.session.add.side_effect = Exception("Erro no Banco")
    user_repository = UserRepository(mock_connection)

    with pytest.raises(Exception):
        user_repository.create_user(username="José", password="123", role="user")

    mock_connection.session.rollback.assert_called_once()

def test_get_users():
    mock_connection = MockConnection()
    user_repository = UserRepository(mock_connection)

    users = user_repository.get_users()

    mock_connection.session.query.assert_called_once_with(User)

    assert users is not None

def test_get_user_by_id():
    mock_connection = MockConnection()
    user_repository = UserRepository(mock_connection)

    user = user_repository.get_user_by_id(1)

    mock_connection.session.query.assert_called_once_with(User)
    mock_connection.session.filter.assert_called_once_with(User.id == 1)
    assert user is not None

def test_get_user_by_username():
    mock_connection = MockConnection()
    user_repository = UserRepository(mock_connection)

    user = user_repository.get_user_by_username("Maria")

    mock_connection.session.query.assert_called_once_with(User)
    mock_connection.session.filter.assert_called_once_with(User.username == "Maria")
    assert user is not None

def test_update_user():
    mock_connection = MockConnection()
    user_repository = UserRepository(mock_connection)

    user_repository.update_user(1, {"password": "abc", "role": "admin"})

    mock_connection.session.query.assert_called_once_with(User)
    mock_connection.session.filter.assert_called_once_with(User.id == 1)
    mock_connection.session.commit.assert_called_once()

def test_error_update_user():
    mock_connection = MockConnection()
    mock_connection.session.query.side_effect = Exception("Erro no Banco")
    user_repository = UserRepository(mock_connection)

    with pytest.raises(Exception):
        user_repository.update_user(1, {"password": "abc", "role": "admin"})

    mock_connection.session.rollback.assert_called_once()

def test_delete_user():
    mock_connection = MockConnection()
    user_repository = UserRepository(mock_connection)

    user_repository.delete_user(2)

    mock_connection.session.query.assert_called_once_with(User)
    mock_connection.session.filter.assert_called_once_with(User.id == 2)
    mock_connection.session.delete.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_error_delete_user():
    mock_connection = MockConnection()
    mock_connection.session.delete.side_effect = Exception("Erro no Banco")
    user_repository = UserRepository(mock_connection)

    with pytest.raises(Exception):
        user_repository.delete_user(2)

    mock_connection.session.rollback.assert_called_once()
