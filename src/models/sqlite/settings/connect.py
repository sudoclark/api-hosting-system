from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    def __init__(self):
        self.__url_database = "sqlite:///database.db"
        self.__engine = None
        self.session = None

    def connect_to_db(self):
        self.__engine = create_engine(url=self.__url_database)

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        make_session = sessionmaker()
        self.session = make_session(bind=self.__engine)
        return self

    def __exit__(self, exc_type, exc, tb):
        self.session.expunge_all()
        self.session.close()

db_manager = DatabaseManager()