from abc import ABC, abstractmethod

class UserInterface():
    """
    Interface dedicada às ações da entidade 'User'. É usado na construção
    e abstração do repositório.
    """
    @abstractmethod
    def create_user(self, username: str, password: str, role: str): pass

    @abstractmethod
    def get_users(self): pass

    @abstractmethod
    def get_user_by_id(self, user_id: int): pass

    @abstractmethod
    def update_user(self, user_id: int, fields: dict): pass

    @abstractmethod
    def delete_user(self, user_id: int): pass
