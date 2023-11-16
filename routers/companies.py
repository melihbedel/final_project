from fastapi import APIRouter, Response, Header, HTTPException
from starlette.responses import JSONResponse

from common.auth import get_user_or_raise_401
from data.models import RegisterDataCompany, LoginData
from routers import helpers
from routers.helpers import username_exists
from service import companies_service, login_service


companies_router = APIRouter(prefix='/companies', tags=['Companies'])


@companies_router.post('/register')
def register(data: RegisterDataCompany):
    if not username_exists(data.username):
        login = login_service.create_login(data.username, data.password, data.type)
        info_id = companies_service.create_company_info(data.id)
        companies_service.create_company(data.name, login.id, info_id)

        return Response(status_code=200, content=f'Success registration {data.username}')

    return JSONResponse(status_code=400, content=f'{data.username} is already taken!')


# @companies_router.get('/company_info')
# def get_info(id: int, x_token: str = Header(default=None)):
#
#     if x_token == None:
#         raise HTTPException(status_code=401,
#                             detail='You must be logged in')
#
#     user = get_user_or_raise_401(x_token)
#
#     if user.type != 1:
#         raise HTTPException(status_code=401,
#                             detail='only company can create company info')

    # if not helpers.id_exists(id, 'users'):
    #     raise HTTPException(status_code=404, detail=f'User with id {id} does not exist.')
    #
    # company_inf_id = companies_service.company_id_info(id)
    # return companies_service.companiy_info(company_inf_id)






