import pytest
from unittest.mock import MagicMock

from tests.controllers.mock_entities_schemas import JOE, MARY
from src.controllers.auth_controller import AuthController

class MockUserRepository:
    def __init__(self):
        self.get_user_by_username = MagicMock(return_value=MARY)

def test_login():
    request_data = {
        "username": "Mary",
        "password": "123"
    }

    mock_repository = MockUserRepository()
    controller = AuthController(mock_repository)

    user = controller.login(request_data)
    response = user.to_dict()

    assert response["username"] == "Mary"
    assert response["role"] == "user"

def test_login_with_empty_request_data():
    request_data = {}

    mock_repository = MockUserRepository()
    controller = AuthController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.login(request_data)

    assert str(ex.value) == "Dados inválidos, confirme os dados enviados."

def test_login_with_missing_field_in_request_data():
    request_data = {
        "username": "Mary"
    }

    mock_repository = MockUserRepository()
    controller = AuthController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.login(request_data)

    assert str(ex.value) == "O nome de usuário e a senha são obrigatórios."

def test_login_when_user_not_found():
    request_data = {
        "username": "Mary",
        "password": "123"
    }

    mock_repository = MockUserRepository()
    mock_repository.get_user_by_username.return_value = None
    controller = AuthController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.login(request_data)

    assert str(ex.value) == "Usuário ou senha inválidos."

def test_login_when_user_sends_wrong_data():
    request_data = {
        "username": "Mary",
        "password": "abc"
    }

    mock_repository = MockUserRepository()
    controller = AuthController(mock_repository)

    with pytest.raises(Exception) as ex:
        controller.login(request_data)

    assert str(ex.value) == "Usuário ou senha inválidos."