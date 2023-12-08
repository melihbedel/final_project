from fastapi import APIRouter, HTTPException, Header, Query
from services.authentication.token_service import verify_token_get_account
from services.professionals import professional_service, company_ads_service
from models.professional import EditProfessional
from models.company_ad import DataCompanyAd
from services import match_service


professionals_router = APIRouter(prefix='/professionals', tags=['Professionals'])


#Professional Profile endpoints

@professionals_router.get('/profile', status_code=200)
def get_professional_info(
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type is not Professional')
    return professional_service.get_professional_by_account_id(account.id)

#---------------------

@professionals_router.put('/profile', status_code=200)
def edit_professional_info(
    updated_info: EditProfessional,
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type is not Professional')
    professional_id = professional_service.get_professional_id_by_account_id(account.id)
    professional_service.verify_professional_update_info(updated_info)
    professional_service.edit_professional(updated_info, professional_id)

    return professional_service.get_professional_by_account_id(account.id)




#Professionals Ad enpoints

@professionals_router.get('/company_ads', status_code=200)
def get_company_ads(
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type is not Professional')
    professional_id = professional_service.get_professional_id_by_account_id(account.id)
    return company_ads_service.get_active_company_ads(professional_id)

#---------------------

@professionals_router.get('/company_ads/{id}', status_code=200)
def get_company_ad_by_id(
    id: int,
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type is not Professional')
    if not company_ads_service.company_ad_exists(id): raise HTTPException(status_code=404, detail=f'Company Ad with id {id} does not exist')
    professional_id = professional_service.get_professional_id_by_account_id(account.id)
    if not professional_service.is_owner(professional_id, id): raise HTTPException(status_code=403, detail='You are not the owner of this ad')
    return company_ads_service.get_company_ad_by_ad_id(id)

#---------------------

@professionals_router.post('/company_ads', status_code=200)
def create_company_ad(
    company_ad: DataCompanyAd,
    x_token: str = Header(default=None)
):
    
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type is not Professional')
    professional_id = professional_service.get_professional_id_by_account_id(account.id)
    company_ads_service.verify_company_ad_info(company_ad)

    return company_ads_service.create_company_ad(company_ad, professional_id)

#---------------------

@professionals_router.put('/company_ads/{id}', status_code=200)
def edit_company_ad(
    id: int,
    updated_company_ad: DataCompanyAd,
    accept_id = Query(None, alias='accept'),
    reject_id = Query(None, alias='reject'),
    x_token: str = Header(default=None)
):
    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type is not Professional')
    if not company_ads_service.company_ad_exists(id): raise HTTPException(status_code=404, detail=f'Company Ad with id {id} does not exist')
    professional_id = professional_service.get_professional_id_by_account_id(account.id)
    if not professional_service.is_owner(professional_id, id): raise HTTPException(status_code=403, detail='You are not the owner of this ad')
    company_ads_service.verify_company_ad_info(updated_company_ad)

    if accept_id and reject_id:
        raise HTTPException(status_code=403, detail='You cannot accept and reject at the same time')
    if accept_id:
        match_service.match_request_exists(id, accept_id)
        response = 'accept'
        match_service.match_response(id, accept_id, response)
    if reject_id:
        match_service.match_request_exists(id, accept_id)
        response = 'reject'
        match_service.match_response(id, reject_id, response)

    return company_ads_service.edit_company_ad(updated_company_ad, id)

#---------------------

@professionals_router.delete('/company_ads/{id}', status_code=200)
def remove_company_ad(
    id: int,
    x_token: str = Header(default=None)
):

    account = verify_token_get_account(x_token)
    if not professional_service.type_is_professional(account.id): raise HTTPException(status_code=400, detail='Account type is not Professional')
    professional_id = professional_service.get_professional_id_by_account_id(account.id)
    if not company_ads_service.company_ad_exists(id): raise HTTPException(status_code=404, detail=f'Company Ad with id {id} does not exist')
    if not professional_service.is_owner(professional_id, id): raise HTTPException(status_code=403, detail='You are not the owner of this ad')

    return company_ads_service.get_active_company_ads(professional_id)