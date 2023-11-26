from data.database import insert_query, read_query, update_query
from data.company import CompanyInfo, CompanyInfoForEdit, Company, JobAds, JobAdsReturn


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


def create_job_ad(job: JobAds, id: int):
    data = insert_query(
        '''INSERT INTO job_ads (salary_min, salary_max, description, location, status, company_id) 
        VALUES(?,?,?,?,?,?)''',
        (job.salary_min, job.salary_max, job.description, job.location, job.status, id))

    return JobAds(id=data, salary_min=job.salary_min, salary_max=job.salary_max, description=job.description,
                  location=job.location, status=job.status)


def counter_active_stat(id, stat: int = 1):
    data = read_query('''SELECT COUNT(*) FROM job_ads WHERE company_id= ? AND status= ?''',
                      (id, stat))
    return data[0][0]


def update_info_status(stat: int, id: int):
    update_query('''UPDATE company_info SET job_ads = ? WHERE companies_id = ?''',
                 (stat, id))


def view_status(id: int, status: int):
    data = read_query('''SELECT * FROM job_ads WHERE company_id = ? AND status = ?''',
                      (id, status))
    print(data)
    return (JobAdsReturn.from_query_result1(*row) for row in data)


def view_job_ad_by_id(id: int, companies_id: int):
    data = read_query('''SELECT * FROM job_ads WHERE company_id = ? AND id = ?''',
                      (companies_id, id))

    return next((JobAds.from_query_result2(*row) for row in data), None)


def edit_jobs_ads(old: JobAds, new: JobAds):
    edited_jobs_ads = JobAdsReturn(
        id=old.id,
        salary_min=new.salary_min,
        salary_max=new.salary_max,
        description=new.description,
        location=new.location,

    )

    update_query(
        '''UPDATE job_ads SET salary_min = ?, salary_max = ?, description = ?, location = ? WHERE id = ?''',
        (edited_jobs_ads.salary_min, edited_jobs_ads.salary_max, edited_jobs_ads.description, edited_jobs_ads.location,
         edited_jobs_ads.id))

    return edited_jobs_ads
