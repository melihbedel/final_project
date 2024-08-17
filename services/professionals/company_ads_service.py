from fastapi import HTTPException
from services.database_service import read_query, insert_query, update_query
from models.company_ad import CompanyAd, DataCompanyAd, Status, PublicCompanyAd
from services import skill_service
from services import match_service


def get_company_ad_by_ad_id(company_ad_id: int):

    ad_data = read_query('SELECT id, professional_id, salary_min, salary_max, description, location, status FROM company_ads WHERE id = ?', (company_ad_id,))
    if not ad_data[0]: raise HTTPException(status_code=404, detail=f'Company Ad with id {company_ad_id} not found')

    skill_id_list = [skill[0] for skill in read_query('SELECT skill_id FROM company_ad_has_skills WHERE company_ad_id = ?', (company_ad_id,))]
    skill_dict = {skill[0]: skill[1] for skill_id in skill_id_list for skill in read_query('SELECT skill, level FROM skills WHERE id = ?', (skill_id,))}
    skill_list = skill_service.list_skills(skill_dict)
    match_requests_lists = match_service.get_all_matches_for_ad_id(company_ad_id)
    match_requests = {'Received': match_requests_lists[1], 'Sent': match_requests_lists[0]}

    result = CompanyAd.from_database(*ad_data[0], skillset = skill_list, match_requests = match_requests)
    return result


def get_public_company_ad_by_ad_id(company_ad_id):
    company_ad = get_company_ad_by_ad_id(company_ad_id)
    if company_ad.status != Status.ACTIVE:
        raise HTTPException(status_code=404, detail=f'Company Ad with id {company_ad_id} not found')

    result = PublicCompanyAd.from_companyad(company_ad)
    return result


def get_active_company_ads(professional_id):
    
    active_company_ads = [get_company_ad_by_ad_id(id) for id_tuple in read_query('SELECT id FROM company_ads WHERE professional_id = ? AND status = ?', (professional_id, 'active')) for id in id_tuple]
    return active_company_ads


def create_company_ad(company_ad_data: DataCompanyAd, professional_id: int):

    company_ad_id = insert_query('INSERT INTO company_ads(professional_id, salary_min, salary_max, description, location, status) VALUES(?,?,?,?,?,?)',
                             (professional_id, company_ad_data.salary_min, company_ad_data.salary_max, company_ad_data.description, company_ad_data.location, Status.ACTIVE))
    
    for skill, level in company_ad_data.skillset.items():
        skill_service.create_skill(skill, level)

    create_company_ad_has_skills(company_ad_id, company_ad_data.skillset)
    company_ad = get_company_ad_by_ad_id(company_ad_id)

    return company_ad


def edit_company_ad(updated_company_ad: DataCompanyAd, company_ad_id: int):
    
    updated_company_ad_dict = updated_company_ad.model_dump(exclude_unset=True)

    for attr, value in updated_company_ad_dict.items():
        if attr == 'skillset':
            edit_company_ad_has_skills(company_ad_id, value)
        else:
            update_query(f'UPDATE company_ads SET {attr} = ? WHERE id = ?', (value, company_ad_id))

    return get_company_ad_by_ad_id(company_ad_id)


def remove_company_ad(company_ad_id: int):
    insert_query('DELETE FROM match_requests WHERE company_ad_id = ?', (company_ad_id,))
    insert_query('DELETE FROM company_ad_has_skills WHERE company_ad_id = ?', (company_ad_id,))
    insert_query('DELETE FROM company_ads WHERE id = ?', (company_ad_id,))



def create_company_ad_has_skills(company_ad_id: int, skillset_dict: dict):

    for skill, level in skillset_dict.items():
        skill_id = skill_service.get_skill_id(skill, level)
        if len(read_query('SELECT company_ad_id, skill_id FROM company_ad_has_skills WHERE company_ad_id = ? AND skill_id = ?', (company_ad_id, skill_id))) < 1:
            insert_query('INSERT INTO company_ad_has_skills(company_ad_id, skill_id) VALUES(?,?)', (company_ad_id, skill_id))


def edit_company_ad_has_skills(company_ad_id: int, skillset_dict: dict):

    current_has_skills_tuples = [tuple 
                                      for skill_id in read_query('SELECT skill_id FROM company_ad_has_skills WHERE company_ad_id = ?', (company_ad_id,)) 
                                      for id in skill_id 
                                      for tuple in read_query('SELECT skill, level FROM skills WHERE id = ?', (id,))]

    for skill, level in skillset_dict.items():
        if level == 'remove':
            if skill in [skill_tuple[0] for skill_tuple in current_has_skills_tuples]:
                remove_company_ad_has_skills(company_ad_id, skill, [tuple[1] for tuple in current_has_skills_tuples if tuple[0] == skill][0])
        else:
            if skill not in [skill_tuple[0] for skill_tuple in current_has_skills_tuples]:
                skill_service.create_skill(skill, level)
                create_company_ad_has_skills(company_ad_id, {skill: level})
            elif level != [skill_tuple[1] for skill_tuple in current_has_skills_tuples if skill_tuple[0] == skill][0]:
                remove_company_ad_has_skills(company_ad_id, 
                                              [skill_tuple[0] for skill_tuple in current_has_skills_tuples if skill_tuple[0] == skill][0],
                                              [skill_tuple[1] for skill_tuple in current_has_skills_tuples if skill_tuple[0] == skill][0])
                skill_service.create_skill(skill, level)
                create_company_ad_has_skills(company_ad_id, {skill: level})


def remove_company_ad_has_skills(company_ad_id, skill, level):
            skill_id = skill_service.get_skill_id(skill, level)
            insert_query('DELETE FROM company_ad_has_skills WHERE company_ad_id = ? AND skill_id = ?', (company_ad_id, skill_id))


def is_company_ad(id: int):
    if id in [company_ad_id_tuple[0] for company_ad_id_tuple in read_query('SELECT id FROM company_ads')]:
        return True
    return False

def get_company_ad_owner(company_ad_id) -> int:
    professional_id = read_query('SELECT professional_id FROM company_ads WHERE id = ?', (company_ad_id,))[0][0]
    
    return professional_id


def verify_company_ad_info(data: DataCompanyAd):
    for attribute in data:
        if attribute[0] == 'description' and isinstance(attribute[1], str):
            if 1 > len(data.description) or len(data.description) > 200: raise HTTPException(status_code=400, detail='Description length must be [1:200]')
        if attribute[0] == 'location' and isinstance(attribute[1], str):
            if 1 > len(data.location) or len(data.location) > 45: raise HTTPException(status_code=400, detail='Location length must be [1:45]')


def company_ad_exists(company_ad_id):
    if read_query('SELECT id FROM company_ads WHERE id = ?', (company_ad_id,)):
        return True
    return False