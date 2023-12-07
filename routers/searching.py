from fastapi import APIRouter, Header, HTTPException

from common.auth import get_user_or_raise_401
from routers.helpers import get_id_by_username, username_exists_type, username_exists
from services.companies_service import find_company_id_by_username_id, company_info
from services.professionals_service import find_pro_id_by_username_id, pro_info
from services.searching_service import view_all_company_ads, view_by_location, view_all_job_ads, \
    view_by_location_job_ads, job_ads_salary_range

searching_router = APIRouter(tags=["Searching"])


@searching_router.get('/Company/company_ads/location', description="Company Searches companies_ad by location!")
def companies_search_for_company_ads(location: str | None = None, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only companies can searching!')

    if location == None:
        return view_all_company_ads()
    else:
        return view_by_location(location)


@searching_router.get('/Company/Professionals/Username', description="Company Searches Professional By Username!")
def companies_search_for_professionals(username: str, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only companies can searching by username!')

    if username_exists_type(username, type=0):
        user_id = get_id_by_username(username)

        pro_id = find_pro_id_by_username_id(user_id)
        pro_inf = pro_info(pro_id)
        result = []
        for data in pro_inf:
            data_dict = {"professional_id": data[-2],
                         "summary": data[0],
                         "location": data[1],
                         "status": data[2],
                         "logo": data[3],
                         "active ads": data[-1]
                         }
            result.append(data_dict)
            return result

    raise HTTPException(status_code=401,
                        detail='Not Found Professional with this username')


@searching_router.get('/professional/Companies/Username', description="Professional Searches companies By Username!")
def professional_search_for_job_ads(username: str, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 0:
        raise HTTPException(status_code=401,
                            detail='Only professional can searching by username!')

    if username_exists_type(username, type=1):
        user_id = get_id_by_username(username)
        companies_id = find_company_id_by_username_id(user_id)
        inf = company_info(companies_id)
        result = []
        for data in inf:
            data_dict = {"companies_id": data[-2],
                         "description": data[0],
                         "location": data[1],
                         "contacts": data[2],
                         "logo": data[3],
                         "active ads": data[-1]
                         }
            result.append(data_dict)
            return result

    raise HTTPException(status_code=401,
                        detail='Not Found Company with this username')


# Professionals can search for job ads (must)
@searching_router.get('/Professional/location', description=" Professional search for jobs-ads by location!")
def professional_search_for_jobs_ads(location: str | None = None, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 0:
        raise HTTPException(status_code=401,
                            detail='Only professional can searching!')

    if location == None:
        return view_all_job_ads()
    else:
        return view_by_location_job_ads(location)


@searching_router.get('/job_ad/salary', description="Salary range for job ads")
def search_job_ads_by_salary_range(min_salary: float = None, max_salary: float = None, threshold: float = 0.0,
                                   x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    if min_salary is not None:
        min_salary = min_salary - (min_salary * round(threshold / 100, 2))
    if max_salary is not None:
        max_salary = max_salary + (max_salary * round(threshold / 100, 2))

    job_ads = job_ads_salary_range(min_salary, max_salary)

    if job_ads is not None:
        return job_ads
    raise HTTPException(status_code=404,
                        detail='you must set at least one of the values')
