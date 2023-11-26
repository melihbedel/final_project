from fastapi import APIRouter, Response, Header, HTTPException, Query
from starlette.responses import JSONResponse

from common.auth import get_user_or_raise_401
from data.company import RegisterDataCompany, CompanyInfoForEdit, JobAds, Status,JobAdsReturn
from routers.helpers import username_exists
from services import companies_service, login_service

companies_router = APIRouter(prefix='/companies', tags=['Companies'])


@companies_router.post('/register')
def register(data: RegisterDataCompany):
    if not username_exists(data.username):
        login = login_service.create_login(data.username, data.password, data.type)
        company_id = companies_service.create_company(data.name, login.id)
        companies_service.create_company_info(company_id.id)

        return Response(status_code=200, content=f'Success registration {data.username}')

    return JSONResponse(status_code=400, content=f'{data.username} is already taken!')


@companies_router.get('/company_info')
def get_info(x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only company can create company info!')

    companies_id = companies_service.find_company_id_by_username_id(user.id)
    company_info = companies_service.company_info(companies_id)
    result = []
    for data in company_info:
        data_dict = {"companies_id": data[-1],
                     "description": data[0],
                     "location": data[1],
                     "contacts": data[2],
                     "logo": data[3],
                     "job_ads": data[4],
                     "matches": data[5]

                     }
        result.append(data_dict)

    return result


@companies_router.put('/edit')
def edit_company(new_company_info: CompanyInfoForEdit, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='only company can edit company info')

    company_id = companies_service.find_company_id_by_username_id(user.id)
    old_company_info = companies_service.company_info(company_id)
    return companies_service.edit_companies(old_company_info, new_company_info)


@companies_router.post('/job_ads')
def crate_job_ads(job: JobAds, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only company can Crate Job ads!')
    companies_id = companies_service.find_company_id_by_username_id(user.id)
    companies_service.create_job_ad(job, companies_id)
    counter_active_status = companies_service.counter_active_stat(companies_id)
    companies_service.update_info_status(counter_active_status, companies_id)

    return Response(status_code=200, content=f'Success create job add!')


@companies_router.get('/jobs_ads')
def get_status(data: Status = Status.active, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only company can view Job ads!')

    companies_id = companies_service.find_company_id_by_username_id(user.id)
    if data.value == "Active":
        status = 1
        return companies_service.view_status(companies_id, status)
    else:
        status = 0
        return companies_service.view_status(companies_id, status)


@companies_router.get('/job_ad/{id}')
def get_job_ad(ids: int = Query(), x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only company can view Job ad!')

    companies_id = companies_service.find_company_id_by_username_id(user.id)
    job_ad = companies_service.view_job_ad_by_id(ids, companies_id)

    if job_ad == None:
        raise HTTPException(status_code=401,
                            detail='You must be insert valid id')
    return job_ad


@companies_router.put('/job_ad/edit/{id}')
def edit_job_ad(new_job_ad: JobAds, ids: int = Query(), x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only company can edit Job ad!')

    company_id = companies_service.find_company_id_by_username_id(user.id)
    old_job_ad = companies_service.view_job_ad_by_id(ids, company_id)

    if old_job_ad == None:
        raise HTTPException(status_code=401,
                            detail='You must be insert valid id')

    return companies_service.edit_jobs_ads(old_job_ad, new_job_ad)
