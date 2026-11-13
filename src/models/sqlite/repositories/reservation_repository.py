from src.models.interfaces.reservation_repository_interface import ReservationInterface
from src.models.sqlite.entities.reservation import Reservation

class ReservationRepository(ReservationInterface):
    def __init__(self, db_connection):
        self.__db_connection = db_connection

    def create_reservation(self, start, end, user_id, hosting_id):
        try:
            with self.__db_connection as db:
                reservation = Reservation(start=start, end=end, user_id=user_id, hosting_id=hosting_id)

                db.session.add(reservation)
                db.session.commit()

        except Exception as ex:
            db.session.rollback()
            raise ex

    def get_reservations(self):
        with self.__db_connection as db:
            reservations = db.session.query(Reservation).all()

            return reservations

    def get_reservation_by_id(self, reservation_id):
        with self.__db_connection as db:
            reservation = db.session.query(Reservation).query(Reservation.id == reservation_id).first()

            return reservation

    def update_reservation(self, reservation_id, fields):
        try:
            with self.__db_connection as db:
                reservation = db.session.query(Reservation).filter(Reservation.id == reservation_id).first()

                for field, value in fields.items():
                    setattr(reservation, field, value)

        except Exception as ex:
            db.session.rollback()
            raise ex

    def delete_reservation(self, reservation_id):
        try:
            with self.__db_connection as db:
                db.session.query(Reservation).filter(Reservation.id == reservation_id).delete()

        except Exception as ex:
            db.session.rollback()
            raise ex