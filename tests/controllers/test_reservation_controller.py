from datetime import datetime, timedelta
from unittest.mock import MagicMock

from src.controllers.reservation_controller import ReservationController
from tests.controllers.mock_entities_schemas import REQUESTER, REQUESTER_USER_ROLE, HOSTING_A, HOSTING_B, RESERVATION_A, RESERVATION_B

class MockHostingRepository:
    def __init__(self):
        self.create_hosting = MagicMock()
        self.get_hosting_by_id = MagicMock(return_value=HOSTING_A)
        self.get_hosting_by_name = MagicMock()
        self.update_hosting = MagicMock()
        self.delete_hosting = MagicMock()

    def get_hostings(self):
        return [
            HOSTING_A,
            HOSTING_B
        ]

class MockReservationRepository:
    def __init__(self):
        self.create_reservation = MagicMock()
        self.get_reservation_by_id = MagicMock()
        self.update_reservation = MagicMock()
        self.delete_reservation = MagicMock()

    def get_reservations(self):
        return [
            RESERVATION_A,
            RESERVATION_B
        ]


def test_create_reservation():
    mock_start = datetime.now() + timedelta(days=1)
    mock_end = mock_start + timedelta(days=3)

    reservation_data = {
        "start": datetime.strftime(mock_start, "%d/%m/%Y"),
        "end": datetime.strftime(mock_end, "%d/%m/%Y"),
        "hosting_name": "Hosting A"
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    controller.create_reservation(reservation_data, REQUESTER)

    mock_reservation_repository.create_reservation.assert_called_once()
    mock_hosting_repository.update_hosting.assert_called_once()
    
def test_get_reservations():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    reservations = controller.get_reservations(REQUESTER)

    assert len(reservations) == 2
    assert reservations[1]["id"] == 2

def test_get_reservation_by_id():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    controller.get_reservation_by_id(1, REQUESTER)

    mock_reservation_repository.get_reservation_by_id.assert_called_once()

def test_update_reservation():
    mock_start = datetime.now() + timedelta(days=3)

    request_data = {
        "start": datetime.strftime(mock_start, "%d/%m/%Y"),
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    controller.update_reservation(request_data, 1, REQUESTER)

    mock_reservation_repository.get_reservation_by_id.assert_called_once()
    mock_reservation_repository.update_reservation.assert_called_once()

def test_delete_reservation():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    controller.delete_reservation(1, REQUESTER)

    mock_reservation_repository.delete_reservation.assert_called_once()
    mock_hosting_repository.update_hosting.assert_called_once()
