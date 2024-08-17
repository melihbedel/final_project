from fastapi import HTTPException
from services.database_service import insert_query, update_query, read_query
from services.professionals import company_ads_service
from models.account import Type
from models.professional import Professional, EditProfessional, Status
from services import match_service


def get_professional_by_id(professional_id):

    professional_data = read_query('SELECT id, first_name, last_name, summary, location, status FROM professionals WHERE id = ?', (professional_id,))[0]
    active_ads_count = len(read_query('SELECT id FROM company_ads WHERE professional_id = ?', (professional_id,)))
    matches_list = match_service.get_all_matches_for_id(professional_id)
    professional = Professional.from_database(*professional_data)
    professional.active_ads = active_ads_count
    professional.match_requests = {'Received': matches_list[1], 'Sent': matches_list[0]}

    professional.match_requests['Sent']


    return professional


def get_professional_by_account_id(account_id):
    professional_id = read_query('SELECT id FROM professionals WHERE account_id = ?', (account_id, ))[0][0]
    return get_professional_by_id(professional_id)


def get_professional_id_by_account_id(account_id):
    return read_query('SELECT id FROM professionals WHERE account_id = ?', (account_id,))[0][0]


def get_all_professionals():
    professionals = [get_professional_by_id(id) for id_tuple in read_query('SELECT id FROM professionals') for id in id_tuple]
    return professionals


def create_professional(account_id: int, first_name: str, last_name: str):
    new_id = insert_query('INSERT INTO professionals(account_id, first_name, last_name, status) VALUES(?,?,?,?)', (account_id, first_name, last_name, Status.ACTIVE))

    return get_professional_by_id(new_id)


def edit_professional(updated_info: EditProfessional, professional_id: int):
    updated_info_dict = updated_info.model_dump(exclude_unset=True)

    for attr, value in updated_info_dict.items():
        update_query(f'UPDATE professionals SET {attr} = ? WHERE id = ?', (value, professional_id))

    return get_professional_by_id(professional_id)


def type_is_professional(account_id) -> bool:
    account_type = read_query('SELECT type FROM accounts WHERE id = ?', (account_id, ))[0][0]

    if account_type == Type.PROFESSIONAL:
        return True
    else:
        return False
    
def verify_professional_update_info(data: EditProfessional):
    for attribute in data:
        if attribute[0] == 'first_name' and isinstance(attribute[1], str):
            if 1 > len(data.first_name) or len(data.first_name) > 45: raise HTTPException(status_code=400, detail='First name length must be [1:45]')
        if attribute[0] == 'last_name' and isinstance(attribute[1], str):
            if 1 > len(data.last_name) or len(data.last_name) > 45: raise HTTPException(status_code=400, detail='Last name length must be [1:45]')
        if attribute[0] == 'summary' and isinstance(attribute[1], str):
            if 1 > len(data.summary) or len(data.summary) > 200: raise HTTPException(status_code=400, detail='Summary length must be [1:200]')
        if attribute[0] == 'location' and isinstance(attribute[1], str):
            if 1 > len(data.location) or len(data.location) > 45: raise HTTPException(status_code=400, detail='Location length must be [1:45]')

def is_owner(professional_id, company_ad_id):
    company_ad = company_ads_service.get_company_ad_by_ad_id(company_ad_id)
    if professional_id == company_ad.professional_id:
        return True
    return False