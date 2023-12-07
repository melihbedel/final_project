from fastapi import APIRouter, Header, HTTPException

from common.auth import get_user_or_raise_401
from routers.helpers import get_id_by_username, username_exists_type
from services.professionals_service import find_pro_id_by_username_id, pro_info
from services.searching_service import view_all_company_ads, view_by_location

searching_router = APIRouter(tags=["Searching"])


@searching_router.get('/company_ads')
def companies_search_for_company_ads(location: str | None = None, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only companies can searching!')

    if location == None:
        return view_all_company_ads()
    else:
        return view_by_location(location)


@searching_router.get('/professionals', description="Company Searches Professional By Username!")
def companies_search_for_professionals(username: str, x_token: str = Header(default=None)):
    if x_token == None:
        raise HTTPException(status_code=401,
                            detail='You must be logged in')

    user = get_user_or_raise_401(x_token)

    if user.type != 1:
        raise HTTPException(status_code=401,
                            detail='Only companies can searching by username!')

    if username_exists_type(username):
        user_id = get_id_by_username(username)
        pro_id = find_pro_id_by_username_id(user_id)
        pro_inf = pro_info(pro_id)
        result = []
        for data in pro_inf:
            data_dict = {"professional_id": data[-2],
                         "summary": data[0],
                         "location": data[1],
                         "status": data[2],
                         "logo": data[3],
                         "active ads": data[-1]
                         }
            result.append(data_dict)
            return result

    raise HTTPException(status_code=401,
                        detail='Not Found Professional with this username')
