from data.database import insert_query
from data.skill_model import DisplaySkill


def create_skill(skill: str, level: str):

    data = insert_query('''INSERT INTO skills (skill, level) VALUES(?,?)''',
                        (skill, level))

    return DisplaySkill(id=data, skill=skill, level=level)


def insert_into(id: int, skill_com: int, user):
    if user == 1:
        insert_query('''INSERT INTO job_ads_has_skills (job_ad_id, Skill_id) VALUES(?,?)''',
                 (id, skill_com))

    else:
        insert_query('''INSERT INTO company_ads_has_skills (company_ad_id, Skill_id) VALUES(?,?)''',
                     (id, skill_com))




