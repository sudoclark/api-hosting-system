from sqlalchemy import Column, INTEGER, String, Numeric
from sqlalchemy.orm import relationship, backref

from src.models.sqlite.settings.base import Base

class Hosting(Base):
    __tablename__ = "hosting"

    id = Column(INTEGER, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    available = Column(INTEGER, nullable=False, default=0)

    #Relationship
    reservations = relationship("Reservation", backref=backref("hosting", lazy="joined"), lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "available": self.available
        }

    def upgrade_availability(self, action: str):
        if action == "book":
            self.available -= 1
        else:
            self.available += 1

        return

    def verify_availability(self):
        if self.available == 0:
            return False

        return True
