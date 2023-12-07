from data.company import JobAds
from data.database import read_query
from data.professional_model import CompanyAds


def view_all_company_ads():
    data = read_query('''SELECT * from company_ads WHERE status = "active"''')

    return (CompanyAds.from_query_result(*row) for row in data)


def view_by_location(location):
    data = read_query('''SELECT * from company_ads WHERE location = ? AND status = "active"''',
                      (location,))

    return (CompanyAds.from_query_result(*row) for row in data)


def view_all_job_ads():
    data = read_query('''SELECT * from job_ads WHERE status = "1"''')

    return (JobAds.from_query_result2(*row) for row in data)


def view_by_location_job_ads(location):
    data = read_query('''SELECT * from job_ads WHERE location = ? AND status = "1"''',
                      (location,))

    return (JobAds.from_query_result2(*row) for row in data)


def job_ads_salary_range(min_salary, max_salary):
    if min_salary is not None and max_salary is not None:
        data = read_query('''SELECT * from job_ads WHERE salary_min >= ? AND salary_max <= ?''',
                          (min_salary, max_salary))
        return (JobAds.from_query_result2(*row) for row in data)


    elif min_salary is not None:
        data = read_query('''SELECT * from job_ads WHERE salary_min >= ?''',
                          (min_salary,))
        return (JobAds.from_query_result2(*row) for row in data)


    elif max_salary is not None:
        data = read_query('''SELECT * from job_ads WHERE salary_max >= ?''',
                          (max_salary,))
        return (JobAds.from_query_result2(*row) for row in data)
