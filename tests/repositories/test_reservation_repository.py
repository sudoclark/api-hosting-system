import pytest
from unittest import mock
from datetime import datetime
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.reservation import Reservation
from src.models.sqlite.repositories.reservation_repository import ReservationRepository

class MockConnection:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(Reservation)],
                    [Reservation(start=datetime(2026, 12, 20), end=datetime(2026, 12, 25), user_id=1, hosting_id=2), Reservation(start=datetime(2026, 11, 23), end=datetime(2026, 11, 30), user_id=2, hosting_id=8)]
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): pass

def test_create_reservation():
    mock_connection = MockConnection()
    repository = ReservationRepository(mock_connection)

    repository.create_reservation(start=datetime(2026, 12, 20), end=datetime(2026, 12, 25), user_id=1, hosting_id=2)

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_error_create_reservation():
    mock_connection = MockConnection()
    mock_connection.session.add.side_effect = Exception("Erro no Banco")
    repository = ReservationRepository(mock_connection)

    with pytest.raises(Exception):
        repository.create_reservation(start=datetime(2026, 12, 20), end=datetime(2026, 12, 25), user_id=1, hosting_id=2)

    mock_connection.session.rollback.assert_called_once()

def test_get_reservations():
    mock_connection = MockConnection()
    repository = ReservationRepository(mock_connection)

    reservations = repository.get_reservations()

    mock_connection.session.query.assert_called_once_with(Reservation)
    mock_connection.session.all.assert_called_once()
    assert len(reservations) == 2

def test_get_reservation_by_id():
    mock_connection = MockConnection()
    repository = ReservationRepository(mock_connection)

    reservation = repository.get_reservation_by_id(2)

    mock_connection.session.query.assert_called_once_with(Reservation)
    mock_connection.session.filter.assert_called_once_with(Reservation.id == 2)
    mock_connection.session.first.assert_called_once()
    assert reservation is not None

def test_update_reservation():
    mock_connection = MockConnection()
    repository = ReservationRepository(mock_connection)

    repository.update_reservation(2, {"start": datetime(2026, 11, 23), "end": datetime(2026, 11, 30)})

    mock_connection.session.query.assert_called_once_with(Reservation)
    mock_connection.session.filter.assert_called_once_with(Reservation.id == 2)
    mock_connection.session.first.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_error_update_reservation():
    mock_connection = MockConnection()
    mock_connection.session.query.side_effect = Exception("Erro no Banco")
    repository = ReservationRepository(mock_connection)

    with pytest.raises(Exception):
        repository.update_reservation(2, {"start": datetime(2026, 11, 23), "end": datetime(2026, 11, 30)})

    mock_connection.session.rollback.assert_called_once()

def test_delete_reservation():
    mock_connection = MockConnection()
    repository = ReservationRepository(mock_connection)

    repository.delete_reservation(5)

    mock_connection.session.query.assert_called_once_with(Reservation)
    mock_connection.session.filter.assert_called_once_with(Reservation.id == 5)
    mock_connection.session.delete.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_error_delete_reservation():
    mock_connection = MockConnection()
    mock_connection.session.delete.side_effect = Exception("Erro no Banco")
    repository = ReservationRepository(mock_connection)

    with pytest.raises(Exception):
        repository.delete_reservation(5)

    mock_connection.session.rollback.assert_called_once()
