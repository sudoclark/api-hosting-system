from src.models.sqlite.entities.user import User
from src.models.sqlite.repositories.hosting_repository import HostingRepository

class HostingController:
    def __init__(self, hosting_repository: HostingRepository):
        self.__hosting_repository = hosting_repository

    def create_hosting(self, hosting_data: dict, requester: User) -> None:
        if not hosting_data:
            raise Exception("Dados inválidos.")

        name = hosting_data.get("name")
        price = hosting_data.get("price")
        available = hosting_data.get("available")

        if requester.role != "admin":
            raise Exception("Você não tem permissão para fazer essa operação.")

        if not name or not price or not available:
            raise Exception("Nome, preço e disponibilidade são dados obrigatórios. Verique as informações enviadas.")

        if not isinstance(price, (float, int)) or price <= 0:
            raise Exception("O preço precisa ser um número inteiro positivo. Ele não pode ser zero.")

        self.__hosting_repository.create_hosting(name=name, price=price, available=available)

    def get_hostings(self) -> list[dict]:
        hostings = self.__hosting_repository.get_hostings()

        return [hosting.to_dict() for hosting in hostings]

    def get_hosting_by_id(self, hosting_id: int) -> dict:
        hosting = self.__hosting_repository.get_hosting_by_id(hosting_id=hosting_id)

        if not hosting:
            raise Exception("Hospedagem não encontrada.")

        return hosting.to_dict()

    def update_hosting(self, request_data: dict, hosting_id: int, requester: User) -> None:
        if requester.role != "admin":
            raise Exception("Você não tem permissão para realizar essa ação. Consulte um administrador.")
        
        if not request_data:
            raise Exception("Valores inválidos, verifique os dados enviados.")
        
        hosting = self.__hosting_repository.get_hosting_by_id(hosting_id=hosting_id)

        if not hosting:
            raise Exception("Hospedagem não encontrada.")

        if "price" in request_data and (not isinstance(request_data["price"], (float, int)) or request_data["price"] <= 0):
            raise Exception("O preço precisa ser um número inteiro positivo. Ele não pode ser zero.")

        fields = ["name", "price", "available"]
        fields_to_update = {}

        for field in fields:
            if field in request_data:
                if not request_data[field]:
                    raise Exception("Dados inválidos, verifique as informações enviadas.")

                fields_to_update[field] = request_data[field]

        self.__hosting_repository.update_hosting(hosting_id=hosting_id, fields=fields_to_update)

    def delete_hosting(self, hosting_id: int, requester: User) -> None:
        if requester.role != "admin":
            raise Exception("Você não tem permissão para realizar essa ação. Consulte um administrador.")

        hosting = self.__hosting_repository.get_hosting_by_id(hosting_id=hosting_id)

        if not hosting:
            raise Exception("Hospedagem não encontrada.")

        self.__hosting_repository.delete_hosting(hosting_id=hosting_id)
