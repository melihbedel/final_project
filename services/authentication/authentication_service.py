from services.authentication.token_service import account_by_username
from services.database_service import insert_query, update_query, read_query
from models.account import Account, Type



def hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()



def create(username: str, password: str, type: Type) -> Account | None:
    password = hash_password(password)
    new_id = insert_query('INSERT INTO accounts(username, password, type) VALUES (?,?,?)', (username, password, type))
    return Account.from_database(new_id, username, '', type)



def login(username: str, password: str) -> Account | None:
    account = account_by_username(username)
    password = hash_password(password)
    return account if account and account.password == password else None


def username_exists(username: str):
    if username in [username_tupel[0] for username_tupel in read_query('SELECT username FROM accounts WHERE username = ?', (username,))]:
        return True
    return False