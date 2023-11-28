from data.database import insert_query, read_query, update_query
from data.models import Professional, ProfessionalInfo, CompanyAds


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


def view_company_ads(pro_id: int):
    data = read_query('''SELECT * from company_ads WHERE professional_id = ?''',
                      (pro_id,))

    return (CompanyAds.from_query_result1(*row) for row in data)


def create_company_ads(company: CompanyAds, pro_id: int):
    data = insert_query(
        '''INSERT INTO company_ads (salary_min, salary_max, description, location, status, professional_id) 
        VALUES(?,?,?,?,?,?)''',
        (company.salary_min, company.salary_max, company.description, company.location, company.status, pro_id))
    return CompanyAds(id=data, salary_min=company.salary_min, salary_max=company.salary_max,
                      description=company.description,
                      location=company.location, status=company.status)


def view_pro_ad_by_id(id: int, pro_id: int):
    data = read_query('''SELECT * FROM company_ads WHERE professional_id = ? AND id = ?''',
                      (pro_id, id))

    return next((CompanyAds.from_query_result(*row) for row in data), None)


def counter_active_stat(pro_id: int, stat="active"):
    data = read_query('''SELECT COUNT(*) FROM company_ads WHERE professional_id= ? AND status= ?''',
                      (pro_id, stat))
    return data[0][0]


def update_pro_info(stat, pro_id):
    update_query('''UPDATE professional_info SET status = ? WHERE professionals_id = ?''',
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
