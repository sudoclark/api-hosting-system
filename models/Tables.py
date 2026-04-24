from database import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')

    reservations = db.relationship("Reservation", backref='reservation', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
    

class Hosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Integer, nullable=False, default=0)

    reservations = db.relationship("Reservation", backref='hosting_reservation', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "available": self.available
        }
    
    def update_availability(self, action):
        if action == "book":
            self.available -= 1
        else:
            self.available += 1
            
        return
    
    def verify_availability(self):
        if self.available == 0:
            return False

        return True
    

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    hosting_id = db.Column(db.Integer, db.ForeignKey("hosting.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "start": datetime.strftime(self.start, "%d/%m/%Y"),
            "end": datetime.strftime(self.end, "%d/%m/%Y"),
            "user_id": self.user_id,
            "hosting_id": self.hosting_id
        }