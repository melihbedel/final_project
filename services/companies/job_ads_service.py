from fastapi import HTTPException
from services.database_service import read_query, insert_query, update_query
from models.job_ad import JobAd, DataJobAd, Status, PublicJobAd
from services import skill_service
from services import match_service


def get_job_ad_by_ad_id(job_ad_id):

    ad_data = read_query('SELECT id, company_id, salary_min, salary_max, description, location, status FROM job_ads WHERE id = ?', (job_ad_id,))
    if not ad_data[0]: raise HTTPException(status_code=404, detail=f'Job Ad with id {job_ad_id} not found')
    
    skill_id_list = [skill[0] for skill in read_query('SELECT skill_id FROM job_ad_required_skills WHERE job_ad_id = ?', (job_ad_id,))]
    skill_dict = {skill[0]: skill[1] for skill_id in skill_id_list for skill in read_query('SELECT skill, level FROM skills WHERE id = ?', (skill_id,))}
    skill_list = skill_service.list_skills(skill_dict)
    match_requests_lists = match_service.get_all_matches_for_ad_id(job_ad_id)
    match_requests = {'Received': match_requests_lists[1], 'Sent': match_requests_lists[0]}

    result = JobAd.from_database(*ad_data[0], requirements = skill_list, match_requests = match_requests)
    return result


def get_public_job_ad_by_ad_id(job_ad_id):
    job_ad = get_job_ad_by_ad_id(job_ad_id)
    if job_ad.status != Status.ACTIVE:
        raise HTTPException(status_code=404, detail=f'Job Ad with id {job_ad_id} not found')

    result = PublicJobAd.from_jobad(job_ad)
    return result


def get_active_job_ads(company_id):

    active_job_ads = [get_job_ad_by_ad_id(id) for id_tuple in read_query('SELECT id FROM job_ads WHERE company_id = ? AND status = ?', (company_id, 'active')) for id in id_tuple]
    return active_job_ads


def get_archived_job_ads(company_id):

    archived_job_ads = [get_job_ad_by_ad_id(id) for id_tuple in read_query('SELECT id FROM job_ads WHERE company_id = ? AND status = ?', (company_id, 'archived')) for id in id_tuple]
    return archived_job_ads 


def create_job_ad(job_ad_data: DataJobAd, company_id: int):

    job_ad_id = insert_query('INSERT INTO job_ads(company_id, salary_min, salary_max, description, location, status) VALUES(?,?,?,?,?,?)',
                             (company_id, job_ad_data.salary_min, job_ad_data.salary_max, job_ad_data.description, job_ad_data.location, Status.ACTIVE))
    
    for skill, level in job_ad_data.requirements.items():
        skill_service.create_skill(skill, level)

    create_job_ad_required_skills(job_ad_id, job_ad_data.requirements)
    job_ad = get_job_ad_by_ad_id(job_ad_id)
    
    return job_ad


def edit_job_ad(updated_job_ad: DataJobAd, job_ad_id: int):
    
    updated_job_ad_dict = updated_job_ad.model_dump(exclude_unset=True)

    for attr, value in updated_job_ad_dict.items():
        if attr == 'requirements':
            edit_job_ad_required_skills(job_ad_id, value)
        else:
            update_query(f'UPDATE job_ads SET {attr} = ? WHERE id = ?', (value, job_ad_id))

    return get_job_ad_by_ad_id(job_ad_id)


def create_job_ad_required_skills(job_ad_id: int, requirements_dict: dict):

    for skill, level in requirements_dict.items():
        skill_id = skill_service.get_skill_id(skill, level)
        if len(read_query('SELECT job_ad_id, skill_id FROM job_ad_required_skills WHERE job_ad_id = ? AND skill_id = ?', (job_ad_id, skill_id))) < 1:
            insert_query('INSERT INTO job_ad_required_skills(job_ad_id, skill_id) VALUES(?,?)', (job_ad_id, skill_id))


def edit_job_ad_required_skills(job_ad_id: int, requirements_dict: dict):

    current_required_skills_tuples = [tuple 
                                      for skill_id in read_query('SELECT skill_id FROM job_ad_required_skills WHERE job_ad_id = ?', (job_ad_id,)) 
                                      for id in skill_id 
                                      for tuple in read_query('SELECT skill, level FROM skills WHERE id = ?', (id,))]

    for skill, level in requirements_dict.items():
        if level == 'remove':
            if skill in [skill_tuple[0] for skill_tuple in current_required_skills_tuples]:
                remove_job_ad_required_skills(job_ad_id, skill, [tuple[1] for tuple in current_required_skills_tuples if tuple[0] == skill][0])
        else:
            if skill not in [skill_tuple[0] for skill_tuple in current_required_skills_tuples]:
                skill_service.create_skill(skill, level)
                create_job_ad_required_skills(job_ad_id, {skill: level})
            elif level != [skill_tuple[1] for skill_tuple in current_required_skills_tuples if skill_tuple[0] == skill][0]:
                remove_job_ad_required_skills(job_ad_id, 
                                              [skill_tuple[0] for skill_tuple in current_required_skills_tuples if skill_tuple[0] == skill][0],
                                              [skill_tuple[1] for skill_tuple in current_required_skills_tuples if skill_tuple[0] == skill][0])
                skill_service.create_skill(skill, level)
                create_job_ad_required_skills(job_ad_id, {skill: level})


def remove_job_ad_required_skills(job_ad_id, skill, level):
            skill_id = skill_service.get_skill_id(skill, level)
            insert_query('DELETE FROM job_ad_required_skills WHERE job_ad_id = ? AND skill_id = ?', (job_ad_id, skill_id))


def is_job_ad(id: int):
    job_ad_ids = [job_ad_id_tuple[0] for job_ad_id_tuple in read_query('SELECT id FROM job_ads')]
    if id in job_ad_ids:
        return True
    return False


def verify_job_ad_info(data: DataJobAd):
    for attribute in data:
        if attribute[0] == 'description' and isinstance(attribute[1], str):
            if 1 > len(data.description) or len(data.description) > 200: raise HTTPException(status_code=400, detail='Description length must be [1:200]')
        if attribute[0] == 'location' and isinstance(attribute[1], str):
            if 1 > len(data.location) or len(data.location) > 45: raise HTTPException(status_code=400, detail='Location length must be [1:45]')


def job_ad_exists(job_ad_id):
    if read_query('SELECT id FROM job_ads WHERE id = ?', (job_ad_id,)):
        return True
    return False