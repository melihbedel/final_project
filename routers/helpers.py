from data.database import read_query


def username_exists(username):
    data = read_query('''SELECT username FROM login_users WHERE username = ?''',
                      (username,))

    return bool(data)


# def id_exists(id: int, table_name: str) -> bool:
#     return any(
#         read_query(
#             f'SELECT id FROM {table_name} where id = ?',
#             (id,)))
