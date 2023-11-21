from fastapi import APIRouter, Header, HTTPException
from starlette.responses import JSONResponse

from data.models import RegisterDataProfessional
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