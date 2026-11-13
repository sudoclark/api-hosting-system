from sqlalchemy import Column, INTEGER, DateTime, ForeignKey
from datetime import datetime

from src.models.sqlite.settings.base import Base

class Reservation(Base):
    __tablename__ = "Reservation"

    id = Column(INTEGER, primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    # Relationships
    user_id = Column(INTEGER, ForeignKey("user.id"), nullable=False)
    hosting_id = Column(INTEGER, ForeignKey("hosting.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "start": datetime.strftime(self.start, "%d/%m/%Y"),
            "end": datetime.strftime(self.end, "%d/%m/%Y"),
            "user_id": self.user_id,
            "hosting_id": self.hosting_id
        }
