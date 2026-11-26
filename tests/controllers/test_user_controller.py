import pytest
from unittest.mock import MagicMock

from src.controllers.user_controller import UserController
from tests.controllers.mock_entities_schemas import REQUESTER, REQUESTER_USER_ROLE, JOE, ANNE

class MockUserRepository:
    def __init__(self):
        self.create_user = MagicMock()
        self.update_user = MagicMock()
        self.delete_user = MagicMock()
        self.get_user_by_id = MagicMock(return_value=JOE)

    def get_users(self):
        return [
            JOE,
            ANNE
        ]


def test_create_user():
    user_data = {
        "username": "Joe",
        "password": "123",
        "role": "user"
    }

    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)
    controller.create_user(user_data)

    mock_repository.create_user.assert_called_once()

def test_create_user_with_none_user_data():
    user_data = {}

    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.create_user(user_data)

    assert str(ex.value) == "Dados inválidos, confirme os dados enviados."

def test_create_user_with_no_username_field():
    user_data = {
        "password": "123"
    }

    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.create_user(user_data)

    assert str(ex.value) == "O nome de usuário e a senha são obrigatórios."

def test_get_users():
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)
    response = controller.get_users(requester=REQUESTER)

    assert len(response) == 2
    assert response[1]["username"] == "Anne"

def test_get_users_when_requester_is_not_admin():
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.get_users(requester=REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não possui permissão para realizar essa ação. Consulte um admin."

def test_get_user_by_id():
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)
    response = controller.get_user_by_id(1, REQUESTER)

    assert response is not None
    assert response["id"] == 1
    assert response["username"] == "Joe"

def test_get_user_by_id_when_requester_is_not_admin():
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.get_user_by_id(user_id=1, requester=REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não possui permissão para realizar essa ação. Consulte um admin."

def test_get_user_by_id_user_not_found():
    mock_repository = MockUserRepository()
    mock_repository.get_user_by_id.return_value = None
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.get_user_by_id(user_id=1, requester=REQUESTER)

    assert str(ex.value) == "Usuário não encontrado."

def test_update_user():
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    controller.update_user(1, {"password": "abc", "role": "admin"}, REQUESTER)

    mock_repository.update_user.assert_called_once()

def test_update_user_when_requester_is_not_admin():
    request_data = {
        "role": "admin"
    }

    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_user(1, request_data, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não possui permissão para realizar essa ação. Consulte um admin."

def test_update_user_with_no_request_data():
    request_data = {}
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_user(1, request_data, REQUESTER)

    assert str(ex.value) == "Dados inválidos, confirme os dados enviados."

def test_update_user_when_user_not_found():
    request_data = {"role": "admin"}
    mock_repository = MockUserRepository()
    mock_repository.get_user_by_id.return_value = None
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_user(1, request_data, REQUESTER)

    assert str(ex.value) == "Usuário não encontrado."

def test_update_user_when_role_is_user_and_id_is_different_then_current_user_id():
    request_data = {"role": "admin"}
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_user(4, request_data, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não tem permissão para mudar seu cargo no sistema"

def test_update_user_when_role_value_is_not_valid():
    request_data = {"role": "batata"}
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_user(4, request_data, REQUESTER)

    assert str(ex.value) == "Valores inválidos, escolha um cargo válido."

def test_update_user_when_password_field_is_empty_in_request_data():
    request_data = {"password": ""}
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.update_user(4, request_data, REQUESTER)

    assert str(ex.value) == "Dados inválidos, verifique as informações enviadas."

def test_delete_user():
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    controller.delete_user(1, REQUESTER)

    mock_repository.delete_user.assert_called_once()

def test_delete_user_when_role_is_user_and_id_is_different_then_current_user_id():
    mock_repository = MockUserRepository()
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.delete_user(1, REQUESTER_USER_ROLE)

    assert str(ex.value) == "Você não possui permissão para realizar essa ação. Consulte um admin."

def test_delete_user_when_user_not_found():
    mock_repository = MockUserRepository()
    mock_repository.get_user_by_id.return_value = None
    controller = UserController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.delete_user(1, REQUESTER)

    assert str(ex.value) == "Usuário não encontrado."
