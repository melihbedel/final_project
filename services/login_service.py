from common.auth import find_by_username
from data.database import insert_query
from data.professional_model import LoginData


def create_login(username: str, password: str, type) -> LoginData | None:
    password = _hash_password(password)

    data = insert_query('''INSERT INTO login_users(username, password, type) VALUES(?,?,?)''',
                        (username, password, type))

    return LoginData(id=data, username=username, password='')


def try_login(username: str, password: str):
    user = find_by_username(username)
    password = _hash_password(password)

    return user if user and user.password == password else None


def _hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()
