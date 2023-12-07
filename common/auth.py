import jwt
from data.database import read_query
from data.professional_model import LoginDataForToken
from fastapi import HTTPException

_JWT_SECRET = ';a3,jhsd1jahe3sd1k3vsfjhas1kv3fsjdh'


def get_user_or_raise_401(token: str) -> LoginDataForToken:

    try:
        payload = is_authenticated(token)
        return find_by_username(payload['username'])
    except:
        raise HTTPException(status_code=401)


def create_token(login: LoginDataForToken) -> str:
    payload = {
        "id": login.id,
        "username": login.username,
        "type": login.type
    }

    return jwt.encode(payload, _JWT_SECRET, algorithm="HS256")


def compare_token(token: str) -> LoginDataForToken:
    try:
        payload = is_authenticated(token)
        payload = find_by_username(payload['username'])
        return payload.id
    except:
        raise HTTPException(status_code=401)


def find_by_username(username: str) -> LoginDataForToken | None:
    data = read_query(
        'SELECT login_user_id, username, password, type FROM login_users WHERE username = ?',
        (username,))

    return next((LoginDataForToken.from_query_result(*row) for row in data), None)


def find_by_id(id: int) -> LoginDataForToken | None:
    data = read_query(
        'SELECT login_user_id, username, password FROM login_users WHERE id = ?',
        (id,))

    return next((LoginDataForToken.from_query_result(*row) for row in data), None)


def is_authenticated(token: str) -> bool:
    return jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
