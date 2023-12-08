from services.database_service import read_query
from models.skill import Skill, Level
from collections import OrderedDict
from services.companies import job_ads_service
from services.professionals import company_ads_service


def get_all_job_ads():
    data = read_query('SELECT id FROM job_ads WHERE status = ?', ('active',))
    job_ads = [job_ads_service.get_public_job_ad_by_ad_id(id[0]) for id in data]

    return job_ads


def get_job_ad_by_id(job_ad_id: int):
    return job_ads_service.get_public_job_ad_by_ad_id(job_ad_id)


def get_all_company_ads():
    data = read_query('SELECT id FROM company_ads WHERE status = ?', ('active',))
    company_ads = [company_ads_service.get_public_company_ad_by_ad_id(id[0]) for id in data]

    return company_ads


def get_company_ad_by_id(company_ad_id: int):
    return company_ads_service.get_public_company_ad_by_ad_id(company_ad_id)


def get_job_ads_for_company_ad(company_ad_id, range_increase: int):
    job_ads = get_all_job_ads()
    company_ad = company_ads_service.get_public_company_ad_by_ad_id(company_ad_id)

    company_ad.salary_min, company_ad.salary_max = change_range(company_ad.salary_min, company_ad.salary_max, range_increase)
    if company_ad.location != 'Remote': company_ad.location = [company_ad.location, 'Remote']

    relevant_job_ads = []

    for job_ad in job_ads:
        if (salary_range_overlap(company_ad, job_ad) and 
            job_ad.location in company_ad.location and
            job_ad.status == 'active' and
            skills_sufficient(company_ad.skillset, job_ad.requirements) == True):
            relevant_job_ads.append(job_ad)

    return relevant_job_ads


def get_company_ads_for_job_ad(job_ad_id, range_increase: int):
    company_ads = get_all_company_ads()
    job_id = job_ads_service.get_public_job_ad_by_ad_id(job_ad_id)

    job_id.salary_min, job_id.salary_max = change_range(job_id.salary_min, job_id.salary_max, range_increase)
    if job_id.location != 'Remote': job_id.location = [job_id.location, 'Remote']

    relevant_company_ads = []

    for company_ad in company_ads:
        if (salary_range_overlap(company_ad, job_id) and 
            company_ad.location in job_id.location and
            company_ad.status == 'active' and
            skills_sufficient(job_id.requirements, company_ad.skillset) == True):
            relevant_company_ads.append(company_ad)

    return relevant_company_ads


def change_range(salary_min, salary_max, percent):

    range = salary_max - salary_min
    change = (range * (percent / 100)) / 2
    salary_min -= change
    salary_max += change

    return (salary_min, salary_max)


def salary_range_overlap(company_ad, job_ad):
    if not (company_ad.salary_max < job_ad.salary_min or
            company_ad.salary_min > job_ad.salary_max):
        return True
    return False


def skills_sufficient(ad_skills: list[Skill], searched_skills: list[Skill]):
    ad_skills: dict = {skill.skill: skill.level for skill in ad_skills}
    searched_skills: dict = {skill.skill: skill.level for skill in searched_skills}

    if not set(searched_skills.keys()):
        return True
    

    for skill in sorted([skill for skill in searched_skills.keys()]):
        if skill not in [skill for skill in ad_skills.keys()]:
            return False
    
    for skill in [skill for skill in searched_skills.keys()]:
        if Level.levels.index(ad_skills[skill]) < Level.levels.index(searched_skills[skill]):
            return False
        
    return True
