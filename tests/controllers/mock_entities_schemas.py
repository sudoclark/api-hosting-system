import bcrypt
from datetime import datetime, timedelta

class MockUserEntity:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }

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

class MockReservationEntity:
    def __init__(self, id, start, end, user_id, hosting_id):
        self.id = id
        self.start = start
        self.end = end
        self.user_id = user_id
        self.hosting_id = hosting_id

    def to_dict(self):
        return {
            "id": self.id,
            "start": datetime.strftime(self.start, "%d/%m/%Y"),
            "end": datetime.strftime(self.end, "%d/%m/%Y"),
            "user_id": self.user_id,
            "hosting_id": self.hosting_id
        }

mock_start = datetime.now() + timedelta(days=1)
mock_end = mock_start + timedelta(days=3)
hashed = bcrypt.hashpw(b"123", bcrypt.gensalt())

JOE = MockUserEntity(id=1, username="Joe", password="123", role="user")
ANNE = MockUserEntity(id=2, username="Anne", password="456", role="user")
MARY = MockUserEntity(id=3, username="Mary", password=hashed, role="user")
HOSTING_A = MockHostingEntity(id=1, name="Hosting A", price=100, available=3)
HOSTING_B = MockHostingEntity(id=2, name="Hosting B", price=250, available=8)
RESERVATION_A = MockReservationEntity(id=1, start=mock_start, end=mock_end, user_id=1, hosting_id=1)
RESERVATION_B = MockReservationEntity(id=2, start=mock_start, end=mock_end, user_id=2, hosting_id=2)
REQUESTER = MockUserEntity(id=3, username="Mary", password="123", role="admin")
REQUESTER_USER_ROLE = MockUserEntity(id=4, username="Carl", password="123", role="user")