from fastapi import APIRouter, Header, HTTPException, Query
from starlette.responses import JSONResponse

from common.auth import get_user_or_raise_401
from data.models import RegisterDataProfessional, ProfessionalInfo, CompanyAds
from routers.helpers import username_exists
from services import login_service, professionals_service

professionals_router = APIRouter(prefix='/professionals', tags=['Professionals'])


@professionals_router.post('/register')
def register(data: RegisterDataProfessional):
    if not username_exists(data.username):
        login = login_service.create_login(data.username, data.password, data.type)
        professional_id = professionals_service.create_pro(data.first_name, data.last_name, login.id)
        professionals_service.create_professional_info(professional_id.id)

        return JSONResponse(status_code=200, content=f'Success registration {data.username}')

    return JSONResponse(status_code=400, content=f'{data.username} is already taken!')


@professionals_router.get('/professional_info')
def get_pro(x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 0:
        raise HTTPException(status_code=401,
                            detail='Only professional can create professional info!')

    professional_id = professionals_service.find_pro_id_by_username_id(user.id)
    pro_info = professionals_service.pro_info(professional_id)
    result = []
    for data in pro_info:
        data_dict = {"professional_id": data[-1],
                     "summary": data[0],
                     "location": data[1],
                     "status": data[2],
                     "logo": data[3],

                     }
        result.append(data_dict)

    return result


@professionals_router.put('/edit')
def edit_pro(new_pro_info: ProfessionalInfo, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 0:
        raise HTTPException(status_code=401,
                            detail='Only professional can edit professional info!')

    pro_id = professionals_service.find_pro_id_by_username_id(user.id)
    old_pro_info = professionals_service.pro_info(pro_id)
    return professionals_service.edit_pro(old_pro_info, new_pro_info)


@professionals_router.get('/company_ads')
def view_all_company_ads(x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 0:
        raise HTTPException(status_code=401,
                            detail='Only professional can view company ads!')

    pro_id = professionals_service.find_pro_id_by_username_id(user.id)
    return professionals_service.view_company_ads(pro_id)


@professionals_router.post('/company_ads')
def crate_company_ads(company: CompanyAds, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 0:
        raise HTTPException(status_code=401,
                            detail='Only professional can create company ads!')

    pro_id = professionals_service.find_pro_id_by_username_id(user.id)
    counter_active_status = professionals_service.counter_active_stat(pro_id)
    professionals_service.update_pro_info(counter_active_status, pro_id)

    return professionals_service.create_company_ads(company, pro_id)


@professionals_router.put('/company_ad/{id}')
def edit_job_ad(new_company_ad: CompanyAds, ids: int = Query(), x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 0:
        raise HTTPException(status_code=401,
                            detail='Only professional can edit Job ad!')

    pro_id = professionals_service.find_pro_id_by_username_id(user.id)
    old_pro_ad = professionals_service.view_pro_ad_by_id(ids, pro_id)

    if old_pro_ad == None:
        raise HTTPException(status_code=401,
                            detail='You must be insert valid id')

    return professionals_service.edit_pro_ads(old_pro_ad, new_company_ad)
