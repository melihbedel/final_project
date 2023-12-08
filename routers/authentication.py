from fastapi import APIRouter, Header, HTTPException
from services.authentication.token_service import create_token
from services.authentication import authentication_service
from services.companies import company_service
from services.professionals import professional_service
from models.account import LoginData, Type
from models.company import RegisterDataCompany
from models.professional import RegisterDataProfessional

authentication_router = APIRouter(prefix='/auth', tags=['Authentication'])


@authentication_router.post('/login')
def login(data: LoginData):

    account = authentication_service.login(data.username, data.password)

    if account:
        token = create_token(account)
        return {'token': token}
    else:
        raise HTTPException(status_code=400, detail='Invalid login data.')


@authentication_router.post('/register')
def register(data: RegisterDataProfessional | RegisterDataCompany, type: Type):


    if authentication_service.username_exists(data.username):
        raise HTTPException(status_code=400, detail='Username taken')
    if 4 > len(data.username) or len(data.username) > 45: raise HTTPException(status_code=400, detail='Allowed username length [4:45]')
    if 4 > len(data.password) or len(data.password) > 45: raise HTTPException(status_code=400, detail='Allowed password length [4:45]')


    if type == 'professional':
        if (1 > len(data.first_name) or len(data.first_name) > 45) or (1 > len(data.last_name) or len(data.last_name) > 45): raise HTTPException(status_code=400, detail='Name length must be [1:45]')
        new_account = authentication_service.create(data.username, data.password, type)
        new_professional = professional_service.create_professional(new_account.id, data.first_name, data.last_name)
        return new_professional


    if type == 'company':
        if 1 > len(data.name) or len(data.name) > 45: raise HTTPException(status_code=400, detail='Name length must be [1:45]')
        new_account = authentication_service.create(data.username, data.password, Type.COMPANY)
        new_company = company_service.create_company(new_account.id, data.name)
        return new_company