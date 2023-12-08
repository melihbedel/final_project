from fastapi import APIRouter, Header, Query, HTTPException
from models.account import Type
from models.match_request import Response
from services import match_service
from services.authentication.token_service import verify_token_get_account
from services import search_service
from services.professionals import professional_service, company_ads_service
from services.companies import company_service, job_ads_service

search_router = APIRouter(prefix='/search', tags=['Search'])


@search_router.get('/job_ads', status_code=200)
def search_job_ads(
    company_id: int = Query(None, alias='company_id'),
    job_ad_id: int = Query(None, alias='ad_id'),
    company_ad_id: int = Query(None, alias='for'),
    salary_range: int = Query(0, alias='salary_range'),
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type must be Professional')

    if company_id:
        return job_ads_service.get_active_job_ads(company_id)
    
    if job_ad_id:
        return search_service.get_job_ad_by_id(job_ad_id)

    if company_ad_id:
        if not company_ads_service.company_ad_exists(company_ad_id): raise HTTPException(status_code=404, detail=f'Company Ad with id {company_ad_id} does not exist')
        professional_id = professional_service.get_professional_id_by_account_id(account.id)
        if not professional_service.is_owner(professional_id, company_ad_id): raise HTTPException(status_code=403, detail=f'You must be the owner of ad {company_ad_id} to request a search')
        return search_service.get_job_ads_for_company_ad(company_ad_id, salary_range)

    return search_service.get_all_job_ads()


@search_router.post('/job_ads/{id}', status_code=200)
def match_job_ad(
    id: int,
    company_ad_id: str = Query(None, alias='match'),
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type must be Professional')
    if not company_ad_id: raise HTTPException(status_code=400, detail='Provide the id of the Company Ad you want to match for')
    if not company_ads_service.company_ad_exists(company_ad_id): raise HTTPException(status_code=404, detail=f'Company Ad with id {company_ad_id} does not exist')
    if not job_ads_service.job_ad_exists(id): raise HTTPException(status_code=404, detail=f'Job Ad with id {id} does not exist')

    professional_id = professional_service.get_professional_id_by_account_id(account.id)
    if not professional_service.is_owner(professional_id, company_ad_id): raise HTTPException(status_code=403, detail=f'You must be the owner of ad {company_ad_id} to initiate a match')

    sender_type = 'professional'
    return match_service.create_match_request(company_ad_id, id, sender_type)





@search_router.get('/company_ads', status_code=200)
def search_company_ads(
    professional_id: int = Query(None, alias='professional_id'),
    company_ad_id: int = Query(None, alias='ad_id'),
    job_ad_id: int = Query(None, alias='for'),
    salary_range: int = Query(0, alias='salary_range'),
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type must be Company')

    if company_ad_id:
        return search_service.get_company_ad_by_id(company_ad_id)
    
    if professional_id:
        return company_ads_service.get_active_company_ads(professional_id)

    if job_ad_id:
        if not job_ads_service.job_ad_exists(job_ad_id): raise HTTPException(status_code=404, detail=f'Job Ad with id {job_ad_id} does not exist')
        company_id = company_service.get_company_id_by_account_id(account.id)
        if not company_service.is_owner(company_id, job_ad_id): raise HTTPException(status_code=403, detail=f'You must be the owner of ad {job_ad_id} to request a search')
        return search_service.get_company_ads_for_job_ad(job_ad_id, salary_range)

    return search_service.get_all_company_ads()


@search_router.post('/company_ads/{id}', status_code=200)
def match_job_ad(
    id: int,
    job_ad_id: str = Query(None, alias='match'),
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type must be Company')
    if not job_ad_id: raise HTTPException(status_code=400, detail='Provide the id of the Job Ad you want to match for')
    if not company_ads_service.company_ad_exists(id): raise HTTPException(status_code=404, detail=f'Company Ad with id {id} does not exist')
    if not job_ads_service.job_ad_exists(job_ad_id): raise HTTPException(status_code=404, detail=f'Job Ad with id {job_ad_id} does not exist')

    company_id = company_service.get_company_id_by_account_id(account.id)
    if not company_service.is_owner(company_id, job_ad_id): raise HTTPException(status_code=403, detail=f'You must be the owner of ad {job_ad_id} to initiate a match')

    sender_type = 'company'
    return match_service.create_match_request(id, job_ad_id, sender_type)


@search_router.get('/companies', status_code=200)
def search_companies(
    company_id: int = Query(None, alias='id'),
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type must be Professional')

    if company_id:
        return company_service.get_company_by_id(company_id)

    return company_service.get_all_companies()


@search_router.get('/professionals', status_code=200)
def search_professionals(
    professional_id: int = Query(None, alias='id'),
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not company_service.type_is_company(account.id): raise HTTPException(status_code=400, detail='Account type must be Company')

    if professional_id:
        return professional_service.get_professional_by_id(professional_id)

    return professional_service.get_all_professionals()