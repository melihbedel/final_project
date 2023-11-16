from data.database import insert_query, read_query
from data.models import Company


def create_company(name: str, login_id, ids):
    data = insert_query('''INSERT INTO companies(name, login_id1, company_info_id) VALUES(?,?,?)''',
                        (name, login_id, ids))

    return Company(id=data, name=name, login_id1=login_id, company_info_id=ids)


def create_company_info(ids):
    data = insert_query('''INSERT INTO company_info (id) VALUES (?)''',
                        (ids,))
    return data


def company_id_info(ids):
    data = read_query('''SELECT company_info_id FROM companies WHERE id = ?''',
                      (ids,))

    return data


# def companiy_info(ids):
#     data = read_query('''SELECT * FROM company_info WHERE id = ?''',
#                       (ids))
#
#     return next((CompanyInfo.from_query_result(*row) for row in data), None)
