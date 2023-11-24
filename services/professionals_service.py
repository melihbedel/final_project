from data.database import insert_query, read_query, update_query
from data.models import Professional, ProfessionalInfo


def create_pro(first_name: str, last_name: str, login_id):
    data = insert_query('''INSERT INTO professionals(first_name, last_name,login_id) VALUES(?,?,?)''',
                        (first_name, last_name, login_id))

    return Professional(id=data, first_name=first_name, last_name=last_name, login_id2=login_id)


def create_professional_info(ids):
    data = insert_query('''INSERT INTO professional_info (professionals_id) VALUES(?)''',
                        (ids,))
    return data


def find_pro_id_by_username_id(id: int):
    data = read_query('''SELECT id FROM professionals WHERE login_id = ?''',
                      (id,))
    return data[0][0]


def pro_info(id: int):
    data = read_query(
        '''SELECT summary, location, status, logo, professionals_id FROM professional_info WHERE professionals_id = ?''',
        (id,))

    return data


def edit_pro(old: ProfessionalInfo, new: ProfessionalInfo):
    edited_company = ProfessionalInfo(
        id=old[0][-1],
        summary=new.summary,
        location=new.location,
        status=new.status,
        logo=new.logo
    )

    update_query(
        '''UPDATE professional_info SET summary = ?, location = ?, status = ?, logo = ? WHERE professionals_id = ?''',
        (edited_company.summary, edited_company.location, edited_company.status, edited_company.logo,
         edited_company.id))

    return edited_company
