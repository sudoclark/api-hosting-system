import bcrypt
from src.models.sqlite.entities.user import User
from src.models.sqlite.repositories.user_repository import UserRepository

class UserController:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def create_user(self, user_data: dict):
        if user_data is None:
            raise Exception("Dados inválidos, confirme os dados enviados.")

        username = user_data.get("username")
        password = user_data.get("password")

        if not username or not password:
            raise Exception("O nome de usuário e a senha são obrigatórios.")

        hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

        self.__user_repository.create_user(username=username, password=hashed, role="user")

    def get_users(self, requester: User):
        if requester.role != "admin":
            raise Exception("Você não possui permissão para realizar essa ação. Consulte um admin.")

        users = self.__user_repository.get_users()

        return [user.to_dict() for user in users]

    def get_user_by_id(self, user_id: int, requester: User):
        if requester.role != "admin":
            raise Exception("Você não possui permissão para realizar essa ação. Consulte um admin.")

        user = self.__user_repository.get_user_by_id(user_id)

        if not user:
            raise Exception("Usuário não encontrado.")

        return user.to_dict()

    def update_user(self, user_id: int, request_data: dict, requester: User):
        if requester.role == "user" and user_id != requester.id:
            raise Exception("Você não possui permissão para realizar essa ação. Consulte um admin.")

        if not request_data:
            raise Exception("Dados inválidos, confirme os dados enviados.")

        user = self.__user_repository.get_user_by_id(user_id)

        if not user:
            raise Exception("Usuário não encontrado.")

        password = request_data.get("password")
        hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt()) if password else None

        fields = ["password", "role"]
        update_fields = {}

        for field in fields:
            if field in request_data:
                if requester.role == "user" and field == "role":
                    raise Exception("Você não tem permissão para mudar seu cargo no sistema")
                if field == "role" and request_data["role"] not in ("admin", "user"):
                    raise Exception("Valores inválidos, escolha um cargo válido.")
                if not request_data[field]:
                    raise Exception("Dados inválidos, verifique as informações enviadas.")

                update_fields[field] = hashed if field == "password" else request_data[field]

        self.__user_repository.update_user(user_id, update_fields)

    def delete_user(self, user_id: int, requester: User):
        if requester.role == "user" and user_id != requester.id:
            raise Exception("Você não possui permissão para realizar essa ação. Consulte um admin.")

        user = self.__user_repository.get_user_by_id(user_id)

        if not user:
            raise Exception("Usuário não encontrado.")

        self.__user_repository.delete_user(user_id)