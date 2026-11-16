from src.models.interfaces.user_repository_interface import UserInterface
from src.models.sqlite.settings.connect import DatabaseManager
from src.models.sqlite.entities.user import User

class UserRepository(UserInterface):
    def __init__(self, db_connection: DatabaseManager):
        self.__db_connection = db_connection

    def create_user(self, username, password, role):
        try:
            with self.__db_connection as db:
                user = User(username=username, password=password, role=role)

                db.session.add(user)
                db.session.commit()

        except Exception as ex:
            db.session.rollback()
            raise ex

    def get_users(self):
        with self.__db_connection as db:
            users = db.session.query(User).all()

            return users

    def get_user_by_id(self, user_id):
        with self.__db_connection as db:
            user = db.session.query(User).filter(User.id == user_id).first()

            return user

    def get_user_by_username(self, username):
        with self.__db_connection as db:
            user = db.session.query(User).filter(User.username == username).first()

            return user

    def update_user(self, user_id, fields):
        try:
            with self.__db_connection as db:
                user = db.session.query(User).filter(User.id == user_id).first()

                for field, value in fields.items():
                    setattr(user, field, value)

                db.session.commit()

        except Exception as ex:
            db.session.rollback()
            raise ex

    def delete_user(self, user_id):
        try:
            with self.__db_connection as db:
                db.session.query(User).filter(User.id == user_id).delete()

                db.session.commit()

        except Exception as ex:
            db.session.rollback()
            raise ex