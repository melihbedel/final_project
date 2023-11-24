from data.database import insert_query, read_query, update_query
from data.models import Company
from data.company_info import CompanyInfo, CompanyInfoForEdit


def create_company(name: str, login_id):
    data = insert_query('''INSERT INTO companies(name, login_id1) VALUES(?,?)''',
                        (name, login_id))

    return Company(id=data, name=name, login_id1=login_id)


def create_company_info(ids):
    data = insert_query('''INSERT INTO company_info (companies_id) VALUES (?)''',
                        (ids,))
    return data


def find_company_id_by_username_id(ids: int):
    data = read_query('''SELECT id FROM companies WHERE login_id1 = ?''',
                      (ids,))
    return data[0][0]


def company_info(id: int):
    data = read_query('''SELECT description, location, contacts, logo, job_ads, matches, companies_id FROM 
    company_info WHERE companies_id = ?''',
                      (id,))
    return data


def edit_companies(old: CompanyInfoForEdit, new: CompanyInfoForEdit):
    print(old)
    edited_company = CompanyInfo(
        id=old[0][-1],
        description=new.description,
        location=new.location,
        contacts=new.contacts,
        logo=new.logo
    )

    update_query(
        '''UPDATE company_info SET description = ?, location = ?, contacts = ?, logo = ? WHERE companies_id = ?''',
        (edited_company.description, edited_company.location, edited_company.contacts, edited_company.logo,
         edited_company.id))

    return edited_company
