import pytest
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

def test_create_reservation_with_empty_request_data():
    reservation_data = {}

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.create_reservation(reservation_data, REQUESTER)

    assert str(ex.value) == "Dados inválidos, confirme os dados enviados."

def test_create_reservation_with_missing_field_on_request_data():
    reservation_data = {
        "hosting_name": "Hosting A"
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.create_reservation(reservation_data, REQUESTER)

    assert str(ex.value) == "Datas de início/fim e o nome da hospedagem são obrigatórios."

def test_create_reservation_when_hosting_not_found():
    mock_start = datetime.now() + timedelta(days=1)
    mock_end = mock_start + timedelta(days=3)

    reservation_data = {
        "start": datetime.strftime(mock_start, "%d/%m/%Y"),
        "end": datetime.strftime(mock_end, "%d/%m/%Y"),
        "hosting_name": "Hosting A"
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    mock_hosting_repository.get_hosting_by_name.return_value = None
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.create_reservation(reservation_data, REQUESTER)

    assert str(ex.value) == "Hospedagem não encontrada."

def test_create_reservation_when_hosting_has_no_availability():
    mock_start = datetime.now() + timedelta(days=1)
    mock_end = mock_start + timedelta(days=3)

    reservation_data = {
        "start": datetime.strftime(mock_start, "%d/%m/%Y"),
        "end": datetime.strftime(mock_end, "%d/%m/%Y"),
        "hosting_name": "Hosting A"
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()

    mock_hosting = MagicMock()
    mock_hosting.verify_availability.return_value = False
    mock_hosting_repository.get_hosting_by_name.return_value = mock_hosting

    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.create_reservation(reservation_data, REQUESTER)

    assert str(ex.value) == "A hospedagem não tem disponibilidade de quartos"

def test_create_reservation_when_start_date_is_bigger_then_end_date():
    reservation_data = {
        "start": "25/11/2026",
        "end": "23/11/2026",
        "hosting_name": "Hosting A"
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.create_reservation(reservation_data, REQUESTER)

    assert str(ex.value) == "A data de início não pode ser maior que a data final."

def test_create_reservation_when_start_date_is_bigger_then_current_date():
    mock_start = datetime.now() - timedelta(days=1)
    mock_end = mock_start + timedelta(days=3)

    reservation_data = {
        "start": datetime.strftime(mock_start, "%d/%m/%Y"),
        "end": datetime.strftime(mock_end, "%d/%m/%Y"),
        "hosting_name": "Hosting A"
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.create_reservation(reservation_data, REQUESTER)

    assert str(ex.value) == "A data de início não pode ser menor que a data atual."
    
def test_get_reservations():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    reservations = controller.get_reservations(REQUESTER)

    assert len(reservations) == 2
    assert reservations[1]["id"] == 2

def test_get_reservations_when_requester_role_is_not_admin():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.get_reservations(REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não tem permissão para realizar essa ação. Contate um administrador."

def test_get_reservation_by_id():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    controller.get_reservation_by_id(1, REQUESTER)

    mock_reservation_repository.get_reservation_by_id.assert_called_once()

def test_get_reservation_by_id_when_reservation_not_found():
    mock_reservation_repository = MockReservationRepository()
    mock_reservation_repository.get_reservation_by_id.return_value = None
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.get_reservation_by_id(1, REQUESTER)

    assert str(ex.value) == "Reserva não encontrada."

def test_get_reservation_by_id_when_requester_role_is_not_admin():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.get_reservation_by_id(1, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não tem permissão para visualizar reservas de outros usuários."

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

def test_update_reservation_with_empty_request_data():
    request_data = {}

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.update_reservation(request_data, 1, REQUESTER)

    assert str(ex.value) == "Dados inválidos, verifique as informações enviadas."

def test_update_reservation_when_reservation_not_found():
    mock_start = datetime.now() + timedelta(days=3)

    request_data = {
        "start": datetime.strftime(mock_start, "%d/%m/%Y"),
    }

    mock_reservation_repository = MockReservationRepository()
    mock_reservation_repository.get_reservation_by_id.return_value = None
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.update_reservation(request_data, 1, REQUESTER)

    assert str(ex.value) == "Reserva não encontrada."

def test_update_reservation_when_requester_role_is_not_admin():
    mock_start = datetime.now() + timedelta(days=3)

    request_data = {
        "start": datetime.strftime(mock_start, "%d/%m/%Y"),
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.update_reservation(request_data, 1, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não tem permissão para atualizar reservas de outros usuários."

def test_update_reservation_when_empty_field_in_request_data():
    request_data = {
        "start": "",
    }

    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.update_reservation(request_data, 1, REQUESTER)

    assert str(ex.value) == "Dados inválidos, verifique as informações enviadas."

def test_delete_reservation():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    controller.delete_reservation(1, REQUESTER)

    mock_reservation_repository.delete_reservation.assert_called_once()
    mock_hosting_repository.update_hosting.assert_called_once()

def test_delete_reservation_when_reservation_not_found():
    mock_reservation_repository = MockReservationRepository()
    mock_reservation_repository.get_reservation_by_id.return_value = None
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.delete_reservation(1, REQUESTER)

    assert str(ex.value) == "Reserva não encontrada."

def test_delete_reservation_when_requester_role_is_not_admin():
    mock_reservation_repository = MockReservationRepository()
    mock_hosting_repository = MockHostingRepository()
    controller = ReservationController(mock_reservation_repository, mock_hosting_repository)

    with pytest.raises(Exception) as ex:
        controller.delete_reservation(1, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não tem permissão para deletar reservas de outros usuários."
