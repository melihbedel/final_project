from fastapi import APIRouter, HTTPException, Header, Query
from services.companies import company_service, job_ads_service
from services import match_service
from services.authentication.token_service import verify_token_get_account
from models.company import EditCompany
from models.job_ad import DataJobAd, Status


companies_router = APIRouter(prefix='/companies', tags=['Companies'])


#Company Profile endpoints

@companies_router.get('/profile', status_code=200)
def get_company_info(
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type is not Company')
    return company_service.get_company_by_account_id(account.id)

#---------------------

@companies_router.put('/profile', status_code=200)
def update_company_info(
    updated_info: EditCompany,
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type is not Company')
    company_id = company_service.get_company_id_by_account_id(account.id)
    company_service.verify_company_update_info(updated_info)
    company_service.edit_company(updated_info, company_id)

    return company_service.get_company_by_id(company_id)




#Job Ad endpoints

@companies_router.get('/job_ads', status_code=200)
def get_job_ads(
    status: Status,
    x_token: str = Header(default=None)
):

    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type is not Company')
    company_id = company_service.get_company_id_by_account_id(account.id)

    if status == 'active':
        return job_ads_service.get_active_job_ads(company_id)
    
    if status == 'archived':
        return job_ads_service.get_archived_job_ads(company_id)

#---------------------

@companies_router.get('/job_ads/{id}', status_code=200)
def get_job_ad_by_id(
    id: int,
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type is not Company')
    if not job_ads_service.job_ad_exists(id): raise HTTPException(status_code=404, detail=f'Job Ad with id {id} does not exist')
    company_id = company_service.get_company_id_by_account_id(account.id)
    if not company_service.is_owner(company_id, id): raise HTTPException(status_code=403, detail='You are not the owner of this ad')
    
    return job_ads_service.get_job_ad_by_ad_id(id)

#---------------------

@companies_router.post('/job_ads', status_code=200)
def create_job_ad(
    job_ad: DataJobAd,
    x_token: str = Header(default=None)
):
    
    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type is not Company')
    company_id = company_service.get_company_id_by_account_id(account.id)
    job_ads_service.verify_job_ad_info(job_ad)

    return job_ads_service.create_job_ad(job_ad, company_id)

#---------------------

@companies_router.put('/job_ads/{id}', status_code=200)
def edit_job_ad(
    id: int,
    updated_job_ad: DataJobAd,
    accept_id = Query(None, alias='accept'),
    reject_id = Query(None, alias='reject'),
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type is not Company')
    if not job_ads_service.job_ad_exists(id): raise HTTPException(status_code=404, detail=f'Job Ad with id {id} does not exist')
    company_id = company_service.get_company_id_by_account_id(account.id)
    if not company_service.is_owner(company_id, id): raise HTTPException(status_code=403, detail='You are not the owner of this ad')
    job_ads_service.verify_job_ad_info(updated_job_ad)

    if accept_id and reject_id:
        raise HTTPException(status_code=403, detail='You cannot accept and reject at the same time')
    if accept_id:
        response = 'accept'
        match_service.match_response(accept_id, id, response)
    if reject_id:
        response = 'reject'
        match_service.match_response(reject_id, id, response)
    
    return job_ads_service.edit_job_ad(updated_job_ad, id)