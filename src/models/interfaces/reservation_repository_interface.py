from abc import ABC, abstractmethod

class ReservationInterface():
    """
    Interface dedicada às ações da entidade 'Reservation'. É usado na construção
    e abstração do repositório.
    """
    @abstractmethod
    def create_reservation(self, start, end, user_id: int, hosting_id: int): pass

    @abstractmethod
    def get_reservations(self): pass

    @abstractmethod
    def get_reservation_by_id(self, reservation_id: int): pass

    @abstractmethod
    def update_reservation(self, reservation_id: int): pass

    @abstractmethod
    def delete_reservation(self, reservation_id: int): pass
