from abc import ABC, abstractmethod

class HostingInterface(ABC):
    """
    Interface dedicada às ações da entidade 'Hosting'. É usado na construção
    e abstração do repositório.
    """
    @abstractmethod
    def create_hosting(self, name: str, price: float, available: bool): pass

    @abstractmethod
    def get_hostings(self): pass

    @abstractmethod
    def get_hosting_by_id(self, hosting_id: int): pass

    @abstractmethod
    def update_hosting(self, hosting_id: int, fields: dict): pass

    @abstractmethod
    def delete_hosting(self, hosting_id: int): pass