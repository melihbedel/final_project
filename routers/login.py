from fastapi import APIRouter, HTTPException

from common.auth import create_token
from data.professional_model import LoginData
from services import login_service

login_router = APIRouter(prefix='/login', tags=['login'])


@login_router.post('/login')
def login(data: LoginData):
    login = login_service.try_login(data.username, data.password)

    if login:
        token = create_token(login)
        return {'token': token}
    else:
        raise HTTPException(status_code=400, detail='Invalid login data.')
