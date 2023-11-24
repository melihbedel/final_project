from fastapi import APIRouter, Header, HTTPException
from starlette.responses import JSONResponse

from common.auth import get_user_or_raise_401
from data.models import RegisterDataProfessional, ProfessionalInfo
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
