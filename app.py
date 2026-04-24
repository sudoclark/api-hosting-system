from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import bcrypt
from datetime import datetime
from functools import wraps

from models.Tables import User, Hosting, Reservation
from utils.ApiUtils import ApiUtils
from database import db

app = Flask(__name__)
resp = ApiUtils.response

app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            return jsonify(resp("ERROR", "Sem permissão!")), 403
        return func(*args, **kwargs)
    return wrapper


## ======================
## ROTAS DE AUTENTICAÇÃO
## ======================

"""
Rotas para autenticação do usuário no sistema.

    Routes:
        load_user(): Após autenticação, faz a busca do usuário no sistema. Ele disponibiliza esse usuário para o 'current_user'.
        login(): Autentica o usuário. Ela salva o 'user_id' nos cookies da sessão para que o usuário seja lembrado.
        logout(): Desloga o usuário.
"""

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)

    return user

@app.route("/login", methods=["POST"])
def login():
    response = request.get_json()

    if not response:
        return jsonify(resp("ERROR", "Dados inválidos, confirme os dados enviados!")), 400
    
    username = response.get("username")
    password = response.get("password")
    
    if not username or not password:
        return jsonify(resp("ERROR", "O nome de usuário e a senha são obrigatórios!")), 400
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify(resp("ERROR", "Usuário não encontrado!")), 404
    
    if not bcrypt.checkpw(str.encode(password), user.password):
        return jsonify(resp("ERROR", "Credenciais inválidas!")), 401
    
    login_user(user)

    return jsonify(resp("SUCCESS", "Usuário autenticado com sucesso!"))

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()

    return jsonify(resp("SUCCESS", "Usuário deslogado com sucesso!"))




## ======================
## ROTAS DO USUÁRIO
## ======================

"""
CRUD dos usuários cadastrados no sistema. Se você for 'admin', consegue listar todos os usuários, editar a senha ou role de qualquer usuário ou deletar qualquer usuário do sistema.
Se a sua permissão for somente 'user', você só consegue listar as informações do seu próprio usuário e editar sua própria senha.

Todas as rotas (com exceção do POST) necessitam de autenticação para serem acessadas.
"""

@app.route("/users", methods=["POST"])
def create_user():
    response = request.json

    if not response:
        return jsonify(resp("ERROR", "Dados inválidos, confirme os dados enviados!")), 400
    
    username = response.get("username")
    password = response.get("password")
    
    if not username or not password:
        return jsonify(resp("ERROR", "O nome de usuário e a senha são obrigatórios!")), 400
    
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

    user = User(username=username, password=hashed, role="user")

    db.session.add(user)
    db.session.commit()

    return jsonify(resp("SUCCESS", "Usuário cadastrado com sucesso!")), 201



@app.route("/users", methods=["GET"])
@login_required
def get_users():
    if current_user.role == "user":
        return jsonify(resp("SUCCESS", "Usuário obtido com sucesso!", user=current_user.to_dict()))
    
    users = User.query.all()

    return jsonify(resp("SUCCESS", "Solicitação bem sucedida!", users=[user.to_dict() for user in users]))


@app.route("/users/<int:id>", methods=["GET"])
@login_required
def get_user_by_id(id):
    if current_user.role == "user" and id != current_user.id:
        return jsonify(resp("ERROR", "Você não tem permissão para essa operação!")), 403
    
    user = User.query.get(id)

    if not user:
        return jsonify(resp("ERROR", "Usuário não encontrado!")), 404

    return jsonify(resp("SUCCESS", "Usuário encontrado!", user=user.to_dict()))


@app.route("/users/<int:id>", methods=["PATCH"])
@login_required
def update_user(id):
    if current_user.role == "user" and id != current_user.id:
        return jsonify(resp("ERROR", "Você não tem permissão para essa operação!")), 403
    
    response = request.json

    if not response:
        return jsonify(resp("ERROR", "Dados inválidos, confirme os dados enviados!")), 400
    
    user = User.query.get(id)

    if not user:
        return jsonify(resp("ERROR", "Usuário não encontrado!")), 404

    password = response.get("password")
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt()) if password else None

    fields = ["password", "role"]

    for field in fields:
        if field in response:
            if not response[field]:
                return jsonify(resp("ERROR", "Dados inválidos!")), 400
            setattr(user, field, hashed if field == "password" else response[field])

    db.session.commit()

    return jsonify(resp("SUCCESS", "Dados alterados com sucesso!"))


@app.route("/users/<int:id>", methods=["DELETE"])
@login_required
def delete_user(id):
    if current_user.role == "user" and id != current_user.id:
        return jsonify(resp("ERROR", "Você não tem permissão para essa operação!")), 403
    
    user = User.query.get(id)

    if not user:
        return jsonify(resp("ERROR", "Usuário não encontrado!")), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify(resp("SUCCESS", "Usuário deletado com sucesso!"))




## ======================
## ROTAS DAS HOSPEDAGENS
## ======================

"""
CRUD para gerenciamento das hospedagens. Aqui conseguimos criar, editar, listar e deletar as hospedagens cadastradas.
Todas as rotas precisam de autenticação e só quem pode realizar essas operações é um administrador do sistema.
"""

@app.route("/hostings", methods=["POST"])
@login_required
def create_hosting():
    response = request.json

    if not response:
        return jsonify(resp("ERROR", "Dados inválidos!")), 400
    
    name = response.get("name")
    price = response.get("price")
    available = response.get("available")

    if current_user.role != "admin":
        return jsonify(resp("ERROR", "Você não tem permissão para fazer essa operação!")), 403
    
    if not isinstance(price, (float, int)) or price <= 0:
        return jsonify(resp("ERROR", "O preço precisa ser um número inteiro positivo. Ele não pode ser zero!")), 400
    
    if not name or not price or not available:
        return jsonify(resp("ERROR", "Nome, preço e disponibilidade são dados obrigatórios. Verique as informações enviadas!")), 400
    
    hosting = Hosting(name=name, price=price, available=available)

    db.session.add(hosting)
    db.session.commit()

    return jsonify(resp("SUCCESS", "Hospedagem adicionada com sucesso!")), 201


@app.route("/hostings", methods=["GET"])
@login_required
@admin_required
def get_hostings():
    hostings = Hosting.query.all()

    return jsonify(resp("SUCCESS", "Listagem realizada com sucesso!", hostings=[host.to_dict() for host in hostings]))


@app.route("/hostings/<int:id>", methods=["GET"])
@login_required
@admin_required
def get_hosting_by_id(id):    
    hosting = Hosting.query.get(id)

    if not hosting:
        return jsonify(resp("ERROR", "Hospedagem não encontrada!")), 404
    
    return jsonify(resp("SUCCESS", "Hospedagem encontrada!", hosting=hosting.to_dict()))


@app.route("/hostings/<int:id>", methods=["PATCH"])
@login_required
@admin_required
def update_hosting(id):
    response = request.json
    
    hosting = Hosting.query.get(id)

    if not hosting:
        return jsonify(resp("ERROR", "Hospedagem não encontrada!")), 404
    
    fields = ["name", "price", "available"]

    for field in fields:
        if field in response:
            if not response[field]:
                return jsonify(resp("ERROR", "Dados inválidos, verifique as informações enviadas!")), 400
            setattr(hosting, field, response[field])

    db.session.commit()

    return jsonify(resp("SUCCESS", "Hospedagem atualizada com sucesso!"))


@app.route("/hostings/<int:id>", methods=["DELETE"])
@login_required
@admin_required
def delete_hosting(id):
    hosting = Hosting.query.get(id)

    if not hosting:
        return jsonify(resp("ERROR", "Hospedagem não encontrada!")), 404
    
    db.session.delete(hosting)
    db.session.commit()

    return jsonify(resp("SUCCESS", "Hospedagem removida com sucesso!"))




## ======================
## ROTAS DAS RESERVAS
## ======================

"""
CRUD para gerenciamento das reservas. Aqui conseguimos criar, editar, listar e deletar as reservas cadastradas.
Todas as rotas precisam de autenticação.

    Permissionamento:
        admin: Consegue criar, listar, atualizar ou deletar uma reserva. Ele tem acesso a todos os dados.
        user: Só consegue visualizar e realizar qualquer ação em sua própria reserva.
"""

@app.route("/reservations", methods=["POST"])
@login_required
def create_reservation():
    response = request.json

    if not response:
        return jsonify(resp("ERROR", "Dados inválidos, confirme os dados enviados!")), 400

    start_str = response.get("start")
    end_str = response.get("end")
    hosting_name = response.get("hosting_name")

    if not start_str or not end_str or not hosting_name:
        return jsonify(resp("ERROR", "Datas de início/fim e o nome da hospedagem são obrigatórios!")), 400

    start = datetime.strptime(start_str, "%d/%m/%Y")
    end = datetime.strptime(end_str, "%d/%m/%Y")

    hosting = Hosting.query.filter_by(name=hosting_name).first()

    if not hosting:
        return jsonify(resp("ERROR", "Hospedagem não encontrada!")), 404
    
    available = hosting.verify_availability()
    
    if not available:
        return jsonify(resp("ERROR", "A hospedagem não tem disponibilidade de quartos!")), 400
    
    if start > end:
        return jsonify(resp("ERROR", "A data de início não pode ser maior que a data final!")), 400
    
    if start < datetime.now():
        return jsonify(resp("ERROR", "A data de início não pode ser menor que a data atual!")), 400
    
    reservation = Reservation(start=start, end=end, user_id=current_user.id, hosting_id=hosting.id)

    hosting.update_availability("book")

    db.session.add(reservation)
    db.session.commit()

    return jsonify(resp("SUCCESS", "Reserva criada com sucesso!")), 201


@app.route("/reservations", methods=["GET"])
@login_required
def get_reservations():
    reservations = Reservation.query.all()

    if current_user.role != "admin":
        return jsonify(resp("SUCCESS", "Listagem das suas reservas", reservations=[res.to_dict() for res in current_user.reservations]))


    return jsonify(resp("SUCCESS", "Listagem obtida com sucesso!", reservations=[res.to_dict() for res in reservations]))


@app.route("/reservations/<int:id>", methods=["GET"])
@login_required
def get_reservation_by_id(id):
    reservation = Reservation.query.get(id)
    
    if not reservation:
        return jsonify(resp("ERROR", "Reserva não encontrada!")), 404

    if current_user.role != "admin" and reservation.user_id != current_user.id:
        return jsonify(resp("ERROR", "Você não tem permissão para visualizar reservas de outros usuários!")), 403
    
    
    return jsonify(resp("SUCCESS", "Reserva localizada com sucesso!", reservation=reservation.to_dict()))


@app.route("/reservations/<int:id>", methods=["PATCH"])
@login_required
def update_reservation(id):
    response = request.json
    
    reservation = Reservation.query.get(id)

    if not reservation:
        return jsonify(resp("ERROR", "Reserva não encontrada!")), 404

    if current_user.role != "admin" and current_user.id != reservation.user_id:
        return jsonify(resp("ERROR", "Você não tem permissão para atualizar reservas de outros usuários!")), 403
    
    fields = ["start", "end"]

    for field in fields:
        if field in response:
            if not response[field]:
                return jsonify(resp("ERROR", "Dados inválidos, verifique as informações enviadas!")), 400
            setattr(reservation, field, datetime.strptime(response[field], "%d/%m/%Y"))

    db.session.commit()

    return jsonify(resp("SUCCESS", "Reserva atualizada com sucesso!"))


@app.route("/reservations/<int:id>", methods=["DELETE"])
@login_required
def delete_reservation(id):
    reservation = Reservation.query.get(id)
    
    if not reservation:
        return jsonify(resp("ERROR", "Reserva não encontrada!")), 404
    
    if current_user.role != "admin" and current_user.id != reservation.user_id:
        return jsonify(resp("ERROR", "Você não tem permissão para deletar reservas de outros usuários!")), 403
    
    hosting = reservation.hosting_reservation

    hosting.update_availability("cancel")
    
    db.session.delete(reservation)
    db.session.commit()

    return jsonify(resp("SUCCESS", "Reserva deletada com sucesso!"))



if __name__ == "__main__":
    app.run(debug=True)