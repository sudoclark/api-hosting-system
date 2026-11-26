import pytest
from unittest.mock import MagicMock

from src.controllers.hosting_controller import HostingController
from tests.controllers.mock_entities_schemas import REQUESTER, REQUESTER_USER_ROLE, HOSTING_A, HOSTING_B
    
class MockHostingRepository:
    def __init__(self):
        self.create_hosting = MagicMock()
        self.get_hosting_by_id = MagicMock(return_value=HOSTING_A)
        self.update_hosting = MagicMock()
        self.delete_hosting = MagicMock()

    def get_hostings(self):
        return [
            HOSTING_A,
            HOSTING_B
        ]
    

def test_create_hosting():
    hosting_data = {
        "name": "Hosting A",
        "price": 250,
        "available": 5
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)
    controller.create_hosting(hosting_data, REQUESTER)

    mock_repository.create_hosting.assert_called_once()

def test_create_hosting_with_empty_request_data():
    hosting_data = {}
    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.create_hosting(hosting_data, REQUESTER)

    assert str(ex.value) == "Dados inválidos."

def test_create_hosting_when_requester_role_is_not_admin():
    hosting_data = {
        "name": "Hosting A",
        "price": 250,
        "available": 5
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.create_hosting(hosting_data, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não tem permissão para fazer essa operação."

def test_create_hosting_with_missing_data():
    hosting_data = {
        "name": "Hosting A",
        "available": 5
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.create_hosting(hosting_data, REQUESTER)

    assert str(ex.value) == "Nome, preço e disponibilidade são dados obrigatórios. Verique as informações enviadas."

def test_create_hosting_with_invalid_price_value():
    hosting_data = {
        "name": "Hosting A",
        "price": "abc",
        "available": 5
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.create_hosting(hosting_data, REQUESTER)

    assert str(ex.value) == "O preço precisa ser um número inteiro positivo. Ele não pode ser zero."

def test_get_hostings():
    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    hostings = controller.get_hostings()

    assert len(hostings) == 2
    assert hostings[1]["name"] == "Hosting B"

def test_get_hosting_by_id():
    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    hosting = controller.get_hosting_by_id(hosting_id=1)

    assert hosting is not None
    assert hosting["name"] == "Hosting A"
    mock_repository.get_hosting_by_id.assert_called_once()

def test_get_hosting_by_id_when_hosting_not_found():
    mock_repository = MockHostingRepository()
    mock_repository.get_hosting_by_id.return_value = None
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.get_hosting_by_id(1)

    assert str(ex.value) == "Hospedagem não encontrada."

def test_update_hosting():
    request_data = {
        "price": 275.90
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)
    controller.update_hosting(request_data, 1, REQUESTER)

    mock_repository.update_hosting.assert_called_once()

def test_update_hosting_when_user_role_is_not_admin():
    request_data = {
        "price": 275.90
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_hosting(request_data, 1, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não tem permissão para realizar essa ação. Consulte um administrador."

def test_update_hosting_with_empty_data():
    request_data = {}

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_hosting(request_data, 1, REQUESTER)

    assert str(ex.value) == "Valores inválidos, verifique os dados enviados."

def test_update_hosting_when_hosting_not_found():
    request_data = {
        "price": 275.90
    }

    mock_repository = MockHostingRepository()
    mock_repository.get_hosting_by_id.return_value = None
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_hosting(request_data, 1, REQUESTER)

    assert str(ex.value) == "Hospedagem não encontrada."

def test_update_hosting_with_negative_price_value():
    request_data = {
        "price": -123
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_hosting(request_data, 1, REQUESTER)

    assert str(ex.value) == "O preço precisa ser um número inteiro positivo. Ele não pode ser zero."

def test_update_hosting_with_empty_field_data():
    request_data = {
        "name": ""
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_hosting(request_data, 1, REQUESTER)

    assert str(ex.value) == "Dados inválidos, verifique as informações enviadas."

def test_delete_hosting():
    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)
    controller.delete_hosting(1, REQUESTER)

    mock_repository.delete_hosting.assert_called_once()

def test_delete_hosting_when_user_role_is_not_admin():
    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.delete_hosting(1, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não tem permissão para realizar essa ação. Consulte um administrador."

def test_delete_hosting_when_hosting_not_found():
    mock_repository = MockHostingRepository()
    mock_repository.get_hosting_by_id.return_value = None
    controller = HostingController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.delete_hosting(1, REQUESTER)

    assert str(ex.value) == "Hospedagem não encontrada."
