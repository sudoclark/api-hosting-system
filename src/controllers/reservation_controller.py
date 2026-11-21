from datetime import datetime

from src.models.sqlite.entities.user import User
from src.models.sqlite.repositories.reservation_repository import ReservationRepository
from src.models.sqlite.repositories.hosting_repository import HostingRepository

class ReservationController:
    def __init__(self, reservation_repository: ReservationRepository, hosting_repository: HostingRepository):
        self.__reservation_repository = reservation_repository
        self.__hosting_repository = hosting_repository

    def create_reservation(self, reservation_data: dict, requester: User) -> None:
        if not reservation_data:
            raise Exception("Dados inválidos, confirme os dados enviados.")

        start_str = reservation_data.get("start")
        end_str = reservation_data.get("end")
        hosting_name = reservation_data.get("hosting_name")

        if not start_str or not end_str or not hosting_name:
            raise Exception("Datas de início/fim e o nome da hospedagem são obrigatórios.")

        start = datetime.strptime(start_str, "%d/%m/%Y")
        end = datetime.strptime(end_str, "%d/%m/%Y")

        hosting = self.__hosting_repository.get_hosting_by_name(hosting_name=hosting_name)

        if not hosting:
            raise Exception("Hospedagem não encontrada.")

        available = hosting.verify_availability()

        if not available:
            raise Exception("A hospedagem não tem disponibilidade de quartos")

        if start > end:
            raise Exception("A data de início não pode ser maior que a data final.")

        if start < datetime.now():
            raise Exception("A data de início não pode ser menor que a data atual.")

        hosting.update_availability("book")

        self.__reservation_repository.create_reservation(start=start, end=end, user_id=requester.id, hosting_id=hosting.id)
        self.__hosting_repository.update_hosting(hosting_id=hosting.id, fields={"available": hosting.available})

    def get_reservations(self, requester: User) -> list[dict]:
        if requester.role != "admin":
            raise Exception("Você não tem permissão para realizar essa ação. Contate um administrador.")
        
        reservations = self.__reservation_repository.get_reservations()

        return [reservation.to_dict() for reservation in reservations]

    def get_reservation_by_id(self, reservation_id: int, requester: User) -> dict:
        reservation = self.__reservation_repository.get_reservation_by_id(reservation_id=reservation_id)

        if not reservation:
            raise Exception("Reserva não encontrada.")
        
        if requester.role != "admin" and reservation.user_id != requester.id:
            raise Exception("Você não tem permissão para visualizar reservas de outros usuários.")

        return reservation.to_dict()

    def update_reservation(self, request_data: dict, reservation_id: int, requester: User) -> None:
        if not request_data:
            raise Exception("Dados inválidos, verifique as informações enviadas.")

        reservation = self.__reservation_repository.get_reservation_by_id(reservation_id=reservation_id)

        if not reservation:
            raise Exception("Reserva não encontrada.")

        if requester.role != "admin" and requester.id != reservation.user_id:
            raise Exception("Você não tem permissão para atualizar reservas de outros usuários.")

        fields = ["start", "end"]
        fields_to_update = {}

        for field in fields:
            if field in request_data:
                if not request_data[field]:
                    raise Exception("Dados inválidos, verifique as informações enviadas.")

                fields_to_update[field] = datetime.strptime(request_data[field], "%d/%m/%Y")

        self.__reservation_repository.update_reservation(reservation_id=reservation_id, fields=fields_to_update)

    def delete_reservation(self, reservation_id: int, requester: User) -> None:
        reservation = self.__reservation_repository.get_reservation_by_id(reservation_id=reservation_id)

        if not reservation:
            raise Exception("Reserva não encontrada.")

        if requester.role != "admin" and requester.id != reservation.user_id:
            raise Exception("Você não tem permissão para deletar reservas de outros usuários.")

        hosting = reservation.hosting
        hosting.update_availability("cancel")

        self.__reservation_repository.delete_reservation(reservation_id=reservation_id)
        self.__hosting_repository.update_hosting(hosting_id=hosting.id, fields={"available": hosting.available})
