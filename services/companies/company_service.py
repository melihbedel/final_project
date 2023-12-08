from fastapi import HTTPException
from services.database_service import insert_query, update_query, read_query
from services.companies import job_ads_service
from models.account import Type
from models.company import Company, EditCompany


def get_company_by_id(company_id):

    company_data = read_query('SELECT id, name, description, location, contacts FROM companies WHERE id = ?', (company_id,))[0]
    active_ads_count = len(read_query('SELECT id FROM job_ads WHERE company_id = ?', (company_id,)))
    matches_count = successful_matches_counter(company_id)
    company = Company.from_database(*company_data)
    company.active_ads = active_ads_count
    company.matches = matches_count

    return company


def get_company_by_account_id(account_id):
    company_id = read_query('SELECT id FROM companies WHERE account_id = ?', (account_id, ))[0][0]
    return get_company_by_id(company_id)


def get_company_id_by_account_id(account_id):
    return read_query('SELECT id FROM companies WHERE account_id = ?', (account_id,))[0][0]


def get_all_companies():
    companies = [get_company_by_id(id) for id_tuple in read_query('SELECT id FROM companies') for id in id_tuple]
    return companies



def create_company(account_id: int, name: str):
    new_id = insert_query('INSERT INTO companies(account_id, name) VALUES(?,?)', (account_id, name))

    return get_company_by_id(new_id)


def edit_company(updated_info: EditCompany, company_id: int):
    updated_info_dict = updated_info.model_dump(exclude_unset=True)

    for attr, value in updated_info_dict.items():
        update_query(f'UPDATE companies SET {attr} = ? WHERE id = ?', (value, company_id))

    return get_company_by_id(company_id)


def successful_matches_counter(company_id) -> int:
    counter = 0

    for job_ad_id_tuple in read_query('SELECT id FROM job_ads WHERE company_id = ?', (company_id,)):
        for job_ad_id in job_ad_id_tuple:
            counter += len(read_query('SELECT * FROM match_requests WHERE job_ad_id = ? AND status = ?', (job_ad_id, 'accepted')))

    return counter


def type_is_company(account_id) -> bool:
    account_type = read_query('SELECT type FROM accounts WHERE id = ?', (account_id, ))[0][0]

    if account_type == Type.COMPANY:
        return True
    else:
        return False


def is_owner(company_id, job_ad_id):
    job_ad = job_ads_service.get_job_ad_by_ad_id(job_ad_id)
    if company_id == job_ad.company_id:
        return True
    return False


def verify_company_update_info(data: EditCompany):
    for attribute in data:
        if attribute[0] == 'name' and isinstance(attribute[1], str):
            if 1 > len(data.name) or len(data.name) > 45: raise HTTPException(status_code=400, detail='Name length must be [1:45]')
        if attribute[0] == 'description' and isinstance(attribute[1], str):
            if 1 > len(data.description) or len(data.description) > 200: raise HTTPException(status_code=400, detail='Description length must be [1:200]')
        if attribute[0] == 'location' and isinstance(attribute[1], str):
            if 1 > len(data.location) or len(data.location) > 45: raise HTTPException(status_code=400, detail='Location length must be [1:45]')
        if attribute[0] == 'contacts' and isinstance(attribute[1], str):
            if (1 > len(data.contacts) or len(data.contacts) > 45) or '@' not in attribute[1]: raise HTTPException(status_code=400, detail='Contact info must be a valid email with length [1:45]')

