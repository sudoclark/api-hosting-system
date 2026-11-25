from unittest.mock import MagicMock

from src.controllers.hosting_controller import HostingController
from tests.controllers.test_user_controller import MockUserEntity

class MockHostingEntity:
    def __init__(self, id, name, price, available):
        self.id = id
        self.name = name
        self.price = price
        self.available = available

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "available": self.available
        }

HOSTING_A = MockHostingEntity(id=1, name="Hosting A", price=100, available=3)
HOSTING_B = MockHostingEntity(id=2, name="Hosting B", price=250, available=8)
REQUESTER = MockUserEntity(id=3, username="Mary", password="123", role="admin")
REQUESTER_USER_ROLE = MockUserEntity(id=4, username="Carl", password="123", role="user")

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

def test_update_hosting():
    request_data = {
        "price": 275.90
    }

    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)
    controller.update_hosting(request_data, 1, REQUESTER)

    mock_repository.update_hosting.assert_called_once()

def test_delete_hosting():
    mock_repository = MockHostingRepository()
    controller = HostingController(mock_repository)
    controller.delete_hosting(1, REQUESTER)

    mock_repository.delete_hosting.assert_called_once()
