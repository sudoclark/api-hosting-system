# Projeto Hospedagem API

API REST para gerenciamento de hospedagens e reservas, desenvolvida com Flask.

## Tecnologias

- Python 3
- Flask 2.3.0
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.2
- bcrypt 5.0.0
- SQLite

## Instalação

```bash
# Clone o repositório e instale as dependências
pip install -r requirements.txt
```

## Executando o projeto

```bash
python3 app.py
```

A API estará disponível em `http://localhost:5000`.

Na primeira execução, crie as tabelas abrindo o shell do Flask:

```bash
flask shell
>>> db.create_all()
>>> db.session.commit()
```

## Autenticação

A API utiliza autenticação por sessão via `flask_login`. Faça login pela rota `/login` e os cookies de sessão serão gerenciados automaticamente pelo cliente.

Existem dois níveis de acesso:

| Role    | Permissões                                              |
|---------|---------------------------------------------------------|
| `user`  | Gerencia apenas seus próprios dados e reservas          |
| `admin` | Acesso total a todos os recursos da API                 |

---

## Rotas

Todas as respostas seguem o formato:

```json
{
  "status": "SUCCESS" | "ERROR",
  "message": "...",
  "..dados.."
}
```

---

### Autenticação

#### `POST /login`
Autentica o usuário e inicia a sessão.

**Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

---

#### `GET /logout`
Encerra a sessão do usuário autenticado.

---

### Usuários

#### `POST /users`
Cria um novo usuário. Não requer autenticação. Todo usuário criado recebe a role `user` por padrão.

**Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

---

#### `GET /users`
Lista usuários. Requer autenticação.

- **admin:** retorna todos os usuários cadastrados.
- **user:** retorna apenas seus próprios dados.

---

#### `GET /users/<id>`
Retorna um usuário pelo ID. Requer autenticação.

- **admin:** pode buscar qualquer usuário.
- **user:** pode buscar apenas seu próprio perfil.

---

#### `PATCH /users/<id>`
Atualiza dados de um usuário. Requer autenticação. Os campos são opcionais — informe apenas o que deseja alterar.

**Body:**
```json
{
  "password": "string",
  "role": "string"
}
```

- **user:** pode alterar apenas sua própria senha.
- **admin:** pode alterar senha e role de qualquer usuário.

---

#### `DELETE /users/<id>`
Remove um usuário. Requer autenticação.

- **admin:** pode deletar qualquer usuário.
- **user:** pode deletar apenas sua própria conta.

---

### Hospedagens

Todas as rotas de hospedagem requerem autenticação e permissão de **admin**.

#### `POST /hostings`
Cadastra uma nova hospedagem.

**Body:**
```json
{
  "name": "string",
  "price": "number",
  "available": "integer"
}
```

---

#### `GET /hostings`
Lista todas as hospedagens cadastradas.

---

#### `GET /hostings/<id>`
Retorna uma hospedagem pelo ID.

---

#### `PATCH /hostings/<id>`
Atualiza dados de uma hospedagem. Os campos são opcionais.

**Body:**
```json
{
  "name": "string",
  "price": "number",
  "available": "integer"
}
```

---

#### `DELETE /hostings/<id>`
Remove uma hospedagem.

---

### Reservas

Todas as rotas de reserva requerem autenticação.

#### `POST /reservations`
Cria uma nova reserva. As datas devem ser informadas no formato `DD/MM/YYYY`.

**Body:**
```json
{
  "hosting_name": "string",
  "start": "DD/MM/YYYY",
  "end": "DD/MM/YYYY"
}
```

Regras:
- A hospedagem precisa ter quartos disponíveis.
- A data de início não pode ser anterior à data atual.
- A data de início não pode ser posterior à data final.

---

#### `GET /reservations`
Lista reservas. 

- **admin:** retorna todas as reservas do sistema.
- **user:** retorna apenas suas próprias reservas.

---

#### `GET /reservations/<id>`
Retorna uma reserva pelo ID.

- **admin:** pode visualizar qualquer reserva.
- **user:** pode visualizar apenas suas próprias reservas.

---

#### `PATCH /reservations/<id>`
Atualiza as datas de uma reserva. Os campos são opcionais.

**Body:**
```json
{
  "start": "DD/MM/YYYY",
  "end": "DD/MM/YYYY"
}
```

- **admin:** pode alterar qualquer reserva.
- **user:** pode alterar apenas suas próprias reservas.

---

#### `DELETE /reservations/<id>`
Remove uma reserva e libera o quarto na hospedagem correspondente.

- **admin:** pode deletar qualquer reserva.
- **user:** pode deletar apenas suas próprias reservas.

---

## Estrutura do projeto

```
projeto_hospedagem/
├── app.py              # Rotas e configuração da aplicação
├── database.py         # Inicialização do SQLAlchemy
├── requirements.txt    # Dependências
├── models/
│   └── Tables.py       # Modelos User, Hosting e Reservation
└── utils/
    └── ApiUtils.py     # Utilitário de resposta padronizada
```
