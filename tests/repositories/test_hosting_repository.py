import pytest
from unittest import mock
from src.models.sqlite.entities.hosting import Hosting
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.repositories.hosting_repository import HostingRepository

class MockConnection:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(Hosting)],
                    [Hosting(name="Hosting A", price=200), Hosting(name="Hosting B", price=150)]
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): pass

def test_create_hosting():
    mock_connection = MockConnection()
    repository = HostingRepository(mock_connection)

    repository.create_hosting("Hosting C", 200, 3)

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_error_create_hosting():
    mock_connection = MockConnection()
    mock_connection.session.add.side_effect = Exception("Erro no Banco")
    repository = HostingRepository(mock_connection)

    with pytest.raises(Exception):
        repository.create_hosting("Hosting C", 200, 3)

    mock_connection.session.rollback.assert_called_once()

def test_get_hostings():
    mock_connection = MockConnection()
    repository = HostingRepository(mock_connection)

    hostings = repository.get_hostings()

    mock_connection.session.query.assert_called_once()
    mock_connection.session.all.assert_called_once()
    assert len(hostings) == 2

def test_get_hosting_by_id():
    mock_connection = MockConnection()
    repository = HostingRepository(mock_connection)

    hosting = repository.get_hosting_by_id(2)

    mock_connection.session.query.assert_called_once_with(Hosting)
    mock_connection.session.filter.assert_called_once_with(Hosting.id == 2)
    mock_connection.session.first.assert_called_once()
    assert hosting is not None

def test_update_hosting():
    mock_connection = MockConnection()
    repository = HostingRepository(mock_connection)

    repository.update_hosting(1, {"name": "Hosting B", "price": 300})

    mock_connection.session.query.assert_called_once_with(Hosting)
    mock_connection.session.filter.assert_called_once_with(Hosting.id == 1)
    mock_connection.session.first.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_error_update_hosting():
    mock_connection = MockConnection()
    mock_connection.session.query.side_effect = Exception("Erro no Banco")
    repository = HostingRepository(mock_connection)

    with pytest.raises(Exception):
        repository.update_hosting(1, {"name": "Hosting B", "price": 300})

    mock_connection.session.rollback.assert_called_once()

def test_delete_hosting():
    mock_connection = MockConnection()
    repository = HostingRepository(mock_connection)

    repository.delete_hosting(3)

    mock_connection.session.query.assert_called_once_with(Hosting)
    mock_connection.session.filter.assert_called_once_with(Hosting.id == 3)
    mock_connection.session.delete.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_error_delete_hosting():
    mock_connection = MockConnection()
    mock_connection.session.delete.side_effect = Exception("Erro no Banco")
    repository = HostingRepository(mock_connection)

    with pytest.raises(Exception):
        repository.delete_hosting(3)

    mock_connection.session.rollback.assert_called_once()
