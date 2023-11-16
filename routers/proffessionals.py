from fastapi import APIRouter
from starlette.responses import JSONResponse

from data.models import RegisterDataProfessional
from routers.helpers import username_exists
from service import login_service, professionals_service

professionals_router = APIRouter(prefix='/professionals', tags=['Professionals'])


@professionals_router.post('/register')
def register(data: RegisterDataProfessional):
    if not username_exists(data.username):
        login = login_service.create_login(data.username, data.password)
        professionals_service.create_pro(data.first_name, data.last_name, login.id)
        return JSONResponse(status_code=200, content=f'Success registration {data.username}')

    return JSONResponse(status_code=400, content=f'{data.username} is already taken!')