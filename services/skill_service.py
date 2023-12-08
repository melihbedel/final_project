from fastapi import HTTPException
from services.database_service import read_query, insert_query, update_query
from models.skill import Skill, Level

def get_skill_id(skill: str, level: str):

    skill_id = read_query('SELECT id FROM skills WHERE skill=? AND level=?', (skill, level))[0][0]
    return skill_id


def get_skill_by_name(skill, level):

    skill_data = read_query('SELECT skill, level FROM skills WHERE skill = ? AND level = ?', (skill, level))
    skill = Skill.from_database(*skill_data[0])
    return skill


def create_skill(skill, level):

    if level not in Level.levels:
        raise HTTPException(status_code=403, detail='A skill can only have the levels "beginner", "advanced" or "expert"')

    if skill_duplicate(skill, level):
        return get_skill_by_name(skill, level)

    insert_query('INSERT INTO skills(skill, level) VALUES(?,?)', (skill, level))
    return get_skill_by_name(skill, level)


def skill_duplicate(skill, level):

    if len(read_query('SELECT * FROM skills WHERE skill = ? AND level = ?', (skill, level))) > 0:
        return True
    return False


def list_skills(skill_dict: dict):
    skill_list = []
    for skill, level in skill_dict.items():
        required_skill = get_skill_by_name(skill, level)
        skill_list.append(required_skill)
    return skill_list
