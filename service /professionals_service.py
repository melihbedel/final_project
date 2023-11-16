from data.database import insert_query
from data.models import Professional


def create_pro(first_name: str, last_name: str, login_id):
    data = insert_query('''INSERT INTO professionals(first_name, last_name,login_id) VALUES(?,?,?)''',
                        (first_name, last_name, login_id))

    return Professional(id=data, first_name=first_name, last_name=last_name, login_id2=login_id)