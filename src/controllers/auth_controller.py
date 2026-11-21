import bcrypt

from src.models.sqlite.repositories.user_repository import UserRepository

class AuthController:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def login(self, request_data: dict) -> None:
        if not request_data:
            raise Exception("Dados inválidos, confirme os dados enviados.")

        username = request_data.get("username")
        password = request_data.get("password")

        if not username or not password:
            raise Exception("O nome de usuário e a senha são obrigatórios.")

        user = self.__user_repository.get_user_by_username(username=username)

        if not user:
            raise Exception("Usuário ou senha inválidos.")

        if not bcrypt.checkpw(str.encode(password), user.password):
            raise Exception("Usuário ou senha inválidos.")

        return user
