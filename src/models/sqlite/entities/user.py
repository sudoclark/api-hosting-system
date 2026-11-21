from sqlalchemy import Column, INTEGER, String, LargeBinary
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin

from src.models.sqlite.settings.base import Base

class User(Base, UserMixin):
    __tablename__ = "user"

    id = Column(INTEGER, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    role = Column(String(80), nullable=False, default="user")

    #Relationship
    reservations = relationship("Reservation", backref=backref("user", lazy="joined"), lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
