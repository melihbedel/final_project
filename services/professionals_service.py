from data.database import insert_query, read_query, update_query
from data.professional_model import Professional, ProfessionalInfo, CompanyAds, ProfessionalInfoForEdit, \
    CompanyAdsForCreate
from data.skill_model import DisplaySkill


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
        '''SELECT summary, location, status, logo, professionals_id, active_ads FROM professional_info WHERE 
        professionals_id = ?''',
        (id,))

    return data


def edit_pro(old: ProfessionalInfo, new: ProfessionalInfoForEdit, status):
    edited_pro = ProfessionalInfo(
        id=old[0][-1],
        summary=new.summary,
        location=new.location,
        status=status,
        logo=new.logo
    )

    update_query(
        '''UPDATE professional_info SET summary = ?, location = ?, status = ?, logo = ? WHERE professionals_id = ?''',
        (edited_pro.summary, edited_pro.location, edited_pro.status, edited_pro.logo,
         edited_pro.id))

    return edited_pro


def view_company_ads(pro_id: int):
    data = read_query('''SELECT * from company_ads RIGHT JOIN (company_ads_has_skills, skills) ON (company_ads.id = company_ads_has_skills.company_ad_id AND company_ads_has_skills.skill_id = skills.id) WHERE professional_id = ?''',
                      (pro_id,))

    return data


def create_company_ads(company: CompanyAdsForCreate, pro_id: int, status):
    data = insert_query(
        '''INSERT INTO company_ads (salary_min, salary_max, description, location, status, professional_id) 
        VALUES(?,?,?,?,?,?)''',
        (company.salary_min, company.salary_max, company.description, company.location, status, pro_id))
    return CompanyAds(id=data, salary_min=company.salary_min, salary_max=company.salary_max,
                      description=company.description,
                      location=company.location, status=status)


def view_pro_ad_by_id(id: int, pro_id: int):
    data = read_query('''SELECT * FROM company_ads WHERE professional_id = ? AND id = ?''',
                      (pro_id, id))

    return next((CompanyAds.from_query_result1(*row) for row in data), None)


def counter_active_stat(pro_id: int, stat="active"):
    data = read_query('''SELECT COUNT(*) FROM company_ads WHERE professional_id= ? AND status= ?''',
                      (pro_id, stat))
    return data[0][0]


def update_pro_info(stat, pro_id):
    update_query('''UPDATE professional_info SET active_ads = ? WHERE professionals_id = ?''',
                 (stat, pro_id))


def edit_pro_ads(old: CompanyAds, new: CompanyAds):
    edited_company_ads = CompanyAds(
        id=old.id,
        salary_min=new.salary_min,
        salary_max=new.salary_max,
        description=new.description,
        location=new.location,
        status=new.status

    )

    update_query(
        '''UPDATE company_ads SET salary_min = ?, salary_max = ?, description = ?, location = ?, status = ? WHERE id 
        = ?''',
        (edited_company_ads.salary_min, edited_company_ads.salary_max, edited_company_ads.description,
         edited_company_ads.location, edited_company_ads.status,
         edited_company_ads.id))

    return edited_company_ads


def create_skill_pro(skill: str, level: str):
    data = insert_query('''INSERT INTO skills (skill, level) VALUES(?,?)''',
                        (skill, level))

    return DisplaySkill(id=data, skill=skill, level=level)
