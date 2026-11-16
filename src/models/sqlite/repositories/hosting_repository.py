from src.models.interfaces.hosting_repository_interface import HostingInterface
from src.models.sqlite.settings.connect import DatabaseManager
from src.models.sqlite.entities.hosting import Hosting

class HostingRepository(HostingInterface):
    def __init__(self, db_connection: DatabaseManager):
        self.__db_connection = db_connection

    def create_hosting(self, name, price, available):
        try:
            with self.__db_connection as db:
                hosting = Hosting(name=name, price=price, available=available)

                db.session.add(hosting)
                db.session.commit()

        except Exception as ex:
            db.session.rollback()
            raise ex

    def get_hostings(self):
        with self.__db_connection as db:
            hostings = db.session.query(Hosting).all()

            return hostings

    def get_hosting_by_id(self, hosting_id):
        with self.__db_connection as db:
            hosting = db.session.query(Hosting).filter(Hosting.id == hosting_id).first()
            
            return hosting

    def update_hosting(self, hosting_id, fields):
        try:
            with self.__db_connection as db:
                hosting = db.session.query(Hosting).filter(Hosting.id == hosting_id).first()

                for field, value in fields.items():
                    setattr(hosting, field, value)

        except Exception as ex:
            db.session.rollback()
            raise ex

    def delete_hosting(self, hosting_id):
        try:
            with self.__db_connection as db:
                db.session.query(Hosting).filter(Hosting.id == hosting_id).delete()

        except Exception as ex:
            db.session.rollback()
            raise ex