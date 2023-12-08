from fastapi import HTTPException
from models.account import Account
from services.database_service import read_query
import jwt


_JWT_SECRET = 'vf13.e,fv.,124,vfd.bnilg.,bn.f.f,gh'


def create_token(account: Account) -> str:

    payload = {
        "id": account.id,
        "username": account.username
    }

    return jwt.encode(payload, _JWT_SECRET, algorithm="HS256")


def decode_token(token: str):

    return jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])


def verify_token_get_account(token: str) -> Account:

    try:
        payload = decode_token(token)
        return account_by_username(payload['username'])
    except:
        raise HTTPException(status_code=401, detail='You must be logged in')


def account_by_username(username: str) -> Account | None:

    data = read_query('SELECT id, username, password, type FROM accounts WHERE username = ?', (username,))

    return next((Account.from_database(*row) for row in data), None)


def account_by_id(id: int) -> Account | None:

    data = read_query('SELECT id, username, password, type FROM accounts WHERE id = ?', (id,))

    return next((Account.from_database(*row) for row in data), None)