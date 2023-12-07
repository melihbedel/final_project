from data.database import read_query


def username_exists(username):
    data = read_query('''SELECT username FROM login_users WHERE username = ?''',
                      (username,))

    return bool(data)


def username_exists_type(username):
    data = read_query('''SELECT username type FROM login_users WHERE username = ? AND type = 0''',
                      (username,))

    return bool(data)


# def id_exists(id: int, table_name: str) -> bool:
#     return any(
#         read_query(
#             f'SELECT id FROM {table_name} where id = ?',
#             (id,)))


def exists(id: int, table_name: str):
    if table_name == 'job_ads':
        data = read_query(f'''SELECT * FROM {table_name} WHERE company_id = ?''',
                          (id,))

    else:
        data = read_query(f'''SELECT * FROM {table_name} WHERE id = ?''',
                          (id,))

    return bool(data)


def get_id_by_username(username):
    data = read_query('''SELECT login_user_id FROM login_users WHERE username = ?''',
                      (username,))

    return data[0][0]
